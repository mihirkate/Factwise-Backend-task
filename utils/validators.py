"""
Validation utilities for input validation and constraint checking.
Industry standard validation with comprehensive error messages.
"""

import re
import uuid
from typing import Any, Dict, List, Optional
from config.settings import get_config

config = get_config()

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class Validator:
    """Centralized validation utilities."""
    
    @staticmethod
    def validate_required_field(value: Any, field_name: str) -> str:
        """
        Validate that a required field is present and not empty.
        
        Args:
            value: Value to validate
            field_name: Name of the field for error messages
            
        Returns:
            Stripped string value
            
        Raises:
            ValidationError: If validation fails
        """
        if value is None:
            raise ValidationError(f"{field_name} is required")
        
        str_value = str(value).strip()
        if not str_value:
            raise ValidationError(f"{field_name} cannot be empty")
        
        return str_value
    
    @staticmethod
    def validate_string_length(value: str, field_name: str, max_length: int) -> str:
        """
        Validate string length constraints.
        
        Args:
            value: String to validate
            field_name: Name of the field for error messages
            max_length: Maximum allowed length
            
        Returns:
            The validated string
            
        Raises:
            ValidationError: If validation fails
        """
        if len(value) > max_length:
            raise ValidationError(f"{field_name} must be <= {max_length} characters")
        
        return value
    
    @staticmethod
    def validate_name(name: str, field_name: str = "Name") -> str:
        """
        Validate name fields (user names, team names, etc.).
        
        Args:
            name: Name to validate
            field_name: Name of the field for error messages
            
        Returns:
            Validated name
            
        Raises:
            ValidationError: If validation fails
        """
        name = Validator.validate_required_field(name, field_name)
        name = Validator.validate_string_length(name, field_name, config.MAX_NAME_LENGTH)
        
        # Additional name validation rules
        if not re.match(r'^[a-zA-Z0-9_-]+$', name):
            raise ValidationError(f"{field_name} can only contain letters, numbers, hyphens, and underscores")
        
        return name
    
    @staticmethod
    def validate_description(description: str, field_name: str = "Description") -> str:
        """
        Validate description fields.
        
        Args:
            description: Description to validate
            field_name: Name of the field for error messages
            
        Returns:
            Validated description
            
        Raises:
            ValidationError: If validation fails
        """
        if description:
            description = description.strip()
            description = Validator.validate_string_length(
                description, field_name, config.MAX_DESCRIPTION_LENGTH
            )
        
        return description or ""
    
    @staticmethod
    def validate_display_name(display_name: str, field_name: str = "Display name", 
                            is_update: bool = False) -> str:
        """
        Validate display name fields.
        
        Args:
            display_name: Display name to validate
            field_name: Name of the field for error messages
            is_update: Whether this is an update operation (allows longer names)
            
        Returns:
            Validated display name
            
        Raises:
            ValidationError: If validation fails
        """
        if display_name:
            display_name = display_name.strip()
            max_length = (config.MAX_DISPLAY_NAME_UPDATE_LENGTH if is_update 
                         else config.MAX_DISPLAY_NAME_LENGTH)
            display_name = Validator.validate_string_length(
                display_name, field_name, max_length
            )
        
        return display_name or ""
    
    @staticmethod
    def validate_uuid(uuid_str: str, field_name: str) -> str:
        """
        Validate UUID format.
        
        Args:
            uuid_str: UUID string to validate
            field_name: Name of the field for error messages
            
        Returns:
            Validated UUID string
            
        Raises:
            ValidationError: If validation fails
        """
        uuid_str = Validator.validate_required_field(uuid_str, field_name)
        
        try:
            uuid.UUID(uuid_str)
            return uuid_str
        except ValueError:
            raise ValidationError(f"{field_name} must be a valid UUID")
    
    @staticmethod
    def validate_status(status: str, valid_statuses: List[str], field_name: str = "Status") -> str:
        """
        Validate status values against allowed options.
        
        Args:
            status: Status to validate
            valid_statuses: List of valid status values
            field_name: Name of the field for error messages
            
        Returns:
            Validated status
            
        Raises:
            ValidationError: If validation fails
        """
        status = Validator.validate_required_field(status, field_name)
        
        if status not in valid_statuses:
            raise ValidationError(f"{field_name} must be one of: {', '.join(valid_statuses)}")
        
        return status
    
    @staticmethod
    def validate_user_list(user_ids: List[str], field_name: str = "User IDs") -> List[str]:
        """
        Validate list of user IDs.
        
        Args:
            user_ids: List of user IDs to validate
            field_name: Name of the field for error messages
            
        Returns:
            Validated list of user IDs
            
        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(user_ids, list):
            raise ValidationError(f"{field_name} must be a list")
        
        if len(user_ids) > config.MAX_TEAM_MEMBERS:
            raise ValidationError(f"Cannot have more than {config.MAX_TEAM_MEMBERS} users")
        
        validated_ids = []
        for user_id in user_ids:
            validated_id = Validator.validate_uuid(user_id, f"{field_name} item")
            validated_ids.append(validated_id)
        
        return validated_ids
