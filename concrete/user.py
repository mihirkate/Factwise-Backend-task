"""
User management implementation with industry standard practices.
Implements UserBase abstract class with comprehensive validation and error handling.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Any, List

from base.user_base import UserBase
from config.settings import get_config
from utils.file_handler import FileHandler
from utils.validators import Validator
from utils.exceptions import (
    ValidationError, ResourceNotFoundError, DuplicateResourceError
)
from utils.logging_config import get_logger

config = get_config()
logger = get_logger(__name__)

class User(UserBase):
    """
    Concrete implementation of UserBase for managing users.
    
    Provides comprehensive user management with validation, error handling,
    and adherence to business rules and constraints.
    """
    
    def __init__(self):
        """Initialize User manager with proper database setup."""
        self.db_path = config.USERS_DB_PATH
        self.teams_db_path = config.TEAMS_DB_PATH
        self._ensure_database_exists()
        logger.info("User manager initialized")
    
    def _ensure_database_exists(self) -> None:
        """Ensure user database file exists with proper structure."""
        try:
            FileHandler.load_json(self.db_path, {"users": []})
        except Exception as e:
            logger.error(f"Failed to initialize user database: {e}")
            raise
    
    def _load_users(self) -> Dict[str, Any]:
        """Load users from database."""
        return FileHandler.load_json(self.db_path, {"users": []})
    
    def _save_users(self, data: Dict[str, Any]) -> None:
        """Save users to database."""
        FileHandler.save_json(self.db_path, data)
    
    def _find_user_by_id(self, users: List[Dict], user_id: str) -> Dict[str, Any]:
        """
        Find user by ID in users list.
        
        Args:
            users: List of user dictionaries
            user_id: ID to search for
            
        Returns:
            User dictionary
            
        Raises:
            ResourceNotFoundError: If user not found
        """
        user = next((u for u in users if u["id"] == user_id), None)
        if not user:
            raise ResourceNotFoundError(f"User with ID {user_id} not found")
        return user
    
    def _check_name_uniqueness(self, users: List[Dict], name: str, exclude_id: str = None) -> None:
        """
        Check if user name is unique.
        
        Args:
            users: List of existing users
            name: Name to check
            exclude_id: User ID to exclude from check (for updates)
            
        Raises:
            DuplicateResourceError: If name already exists
        """
        existing_user = next(
            (u for u in users if u["name"] == name and u["id"] != exclude_id), 
            None
        )
        if existing_user:
            raise DuplicateResourceError("User name must be unique")
    
    def create_user(self, request: str) -> str:
        """
        Create a new user with unique name validation.
        
        Args:
            request: JSON string with user details
            
        Returns:
            JSON string with created user ID
            
        Raises:
            ValidationError: If input validation fails
            DuplicateResourceError: If user name already exists
        """
        logger.info("Creating new user")
        
        try:
            data = json.loads(request)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in create_user request: {e}")
            raise ValidationError("Invalid JSON format")
        
        try:
            # Validate input
            name = Validator.validate_name(data.get("name", ""), "User name")
            display_name = Validator.validate_display_name(
                data.get("display_name", ""), "Display name"
            )
            
            # Load existing users and check uniqueness
            db_data = self._load_users()
            users = db_data.get("users", [])
            self._check_name_uniqueness(users, name)
            
            # Create new user
            user_id = str(uuid.uuid4())
            new_user = {
                "id": user_id,
                "name": name,
                "display_name": display_name or name,
                "creation_time": datetime.now().isoformat()
            }
            
            users.append(new_user)
            db_data["users"] = users
            self._save_users(db_data)
            
            logger.info(f"User created successfully: {user_id}")
            return json.dumps({"id": user_id})
            
        except (ValidationError, DuplicateResourceError) as e:
            logger.warning(f"User creation failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in create_user: {e}")
            raise ValidationError("Failed to create user")
    
    def list_users(self) -> str:
        """
        List all users.
        
        Returns:
            JSON string with list of users
        """
        logger.debug("Listing all users")
        
        try:
            db_data = self._load_users()
            users = db_data.get("users", [])
            
            result = []
            for user in users:
                result.append({
                    "name": user["name"],
                    "display_name": user["display_name"],
                    "creation_time": user["creation_time"]
                })
            
            logger.debug(f"Listed {len(result)} users")
            return json.dumps(result)
            
        except Exception as e:
            logger.error(f"Failed to list users: {e}")
            raise ValidationError("Failed to retrieve users")
    
    def describe_user(self, request: str) -> str:
        """
        Get details of a specific user.
        
        Args:
            request: JSON string with user ID
            
        Returns:
            JSON string with user details
            
        Raises:
            ValidationError: If input validation fails
            ResourceNotFoundError: If user not found
        """
        logger.debug("Describing user")
        
        try:
            data = json.loads(request)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in describe_user request: {e}")
            raise ValidationError("Invalid JSON format")
        
        try:
            user_id = Validator.validate_uuid(data.get("id", ""), "User ID")
            
            db_data = self._load_users()
            users = db_data.get("users", [])
            user = self._find_user_by_id(users, user_id)
            
            result = {
                "name": user["name"],
                "display_name": user["display_name"],
                "creation_time": user["creation_time"]
            }
            
            logger.debug(f"User described: {user_id}")
            return json.dumps(result)
            
        except (ValidationError, ResourceNotFoundError) as e:
            logger.warning(f"User description failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in describe_user: {e}")
            raise ValidationError("Failed to retrieve user details")
    
    def update_user(self, request: str) -> str:
        """
        Update user details (name cannot be changed).
        
        Args:
            request: JSON string with user update details
            
        Returns:
            JSON string with success status
            
        Raises:
            ValidationError: If input validation fails or name change attempted
            ResourceNotFoundError: If user not found
        """
        logger.info("Updating user")
        
        try:
            data = json.loads(request)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in update_user request: {e}")
            raise ValidationError("Invalid JSON format")
        
        try:
            user_id = Validator.validate_uuid(data.get("id", ""), "User ID")
            user_data = data.get("user", {})
            
            # Validate input
            name = user_data.get("name", "").strip()
            display_name = Validator.validate_display_name(
                user_data.get("display_name", ""), "Display name", is_update=True
            )
            
            db_data = self._load_users()
            users = db_data.get("users", [])
            user_index = next((i for i, u in enumerate(users) if u["id"] == user_id), None)
            
            if user_index is None:
                raise ResourceNotFoundError("User not found")
            
            # Check if name change is attempted (not allowed)
            if name and name != users[user_index]["name"]:
                raise ValidationError("User name cannot be updated")
            
            # Update display name only
            if display_name:
                users[user_index]["display_name"] = display_name
            
            db_data["users"] = users
            self._save_users(db_data)
            
            logger.info(f"User updated successfully: {user_id}")
            return json.dumps({"status": "success"})
            
        except (ValidationError, ResourceNotFoundError) as e:
            logger.warning(f"User update failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in update_user: {e}")
            raise ValidationError("Failed to update user")
    
    def get_user_teams(self, request: str) -> str:
        """
        Get teams that a user belongs to.
        
        Args:
            request: JSON string with user ID
            
        Returns:
            JSON string with list of user's teams
            
        Raises:
            ValidationError: If input validation fails
            ResourceNotFoundError: If user not found
        """
        logger.debug("Getting user teams")
        
        try:
            data = json.loads(request)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in get_user_teams request: {e}")
            raise ValidationError("Invalid JSON format")
        
        try:
            user_id = Validator.validate_uuid(data.get("id", ""), "User ID")
            
            # Check if user exists
            db_data = self._load_users()
            users = db_data.get("users", [])
            self._find_user_by_id(users, user_id)
            
            # Load teams and find user's teams
            teams_data = FileHandler.load_json(self.teams_db_path, {"teams": []})
            teams = teams_data.get("teams", [])
            
            user_teams = []
            for team in teams:
                if user_id in team.get("members", []):
                    user_teams.append({
                        "name": team["name"],
                        "description": team["description"],
                        "creation_time": team["creation_time"]
                    })
            
            logger.debug(f"Found {len(user_teams)} teams for user {user_id}")
            return json.dumps(user_teams)
            
        except (ValidationError, ResourceNotFoundError) as e:
            logger.warning(f"Get user teams failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_user_teams: {e}")
            raise ValidationError("Failed to retrieve user teams")