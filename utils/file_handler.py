"""
File handling utilities for JSON data persistence.
Industry standard utilities with proper error handling and logging.
"""

import json
import os
import logging
from typing import Dict, Any, Optional
from config.settings import get_config

logger = logging.getLogger(__name__)
config = get_config()

class FileHandler:
    """Centralized file handling operations for JSON persistence."""
    
    @staticmethod
    def ensure_directory_exists(path: str) -> None:
        """Ensure directory exists, create if it doesn't."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            logger.debug(f"Directory ensured for path: {path}")
        except Exception as e:
            logger.error(f"Failed to create directory for {path}: {e}")
            raise
    
    @staticmethod
    def load_json(path: str, default_structure: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Load JSON data from file with error handling.
        
        Args:
            path: File path to load from
            default_structure: Default structure if file doesn't exist
            
        Returns:
            Dictionary containing loaded data
            
        Raises:
            ValueError: If JSON is malformed
            IOError: If file operation fails
        """
        try:
            if not os.path.exists(path):
                logger.info(f"File not found, creating with default structure: {path}")
                default = default_structure or {}
                FileHandler.save_json(path, default)
                return default
            
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
                logger.debug(f"Successfully loaded data from: {path}")
                return data
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format in file {path}: {e}")
            raise ValueError(f"Invalid JSON format in file {path}: {e}")
        except Exception as e:
            logger.error(f"Failed to load file {path}: {e}")
            raise IOError(f"Failed to load file {path}: {e}")
    
    @staticmethod
    def save_json(path: str, data: Dict[str, Any]) -> None:
        """
        Save data to JSON file with error handling.
        
        Args:
            path: File path to save to
            data: Data to save
            
        Raises:
            IOError: If file operation fails
        """
        try:
            FileHandler.ensure_directory_exists(path)
            
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
                logger.debug(f"Successfully saved data to: {path}")
                
        except Exception as e:
            logger.error(f"Failed to save file {path}: {e}")
            raise IOError(f"Failed to save file {path}: {e}")
    
    @staticmethod
    def backup_file(path: str) -> str:
        """
        Create a backup of the file.
        
        Args:
            path: Original file path
            
        Returns:
            Backup file path
        """
        try:
            if not os.path.exists(path):
                return ""
            
            backup_path = f"{path}.backup"
            data = FileHandler.load_json(path)
            FileHandler.save_json(backup_path, data)
            logger.info(f"Backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Failed to create backup for {path}: {e}")
            raise
