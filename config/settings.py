"""
Configuration settings for Team Project Planner.
Industry standard configuration management with environment-based settings.
"""

import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Base configuration class with common settings."""
    
    # Database Configuration
    DB_DIR = os.path.join(BASE_DIR, "db")
    USERS_DB_PATH = os.path.join(DB_DIR, "users.json")
    TEAMS_DB_PATH = os.path.join(DB_DIR, "teams.json")
    BOARDS_DB_PATH = os.path.join(DB_DIR, "boards.json")
    TASKS_DB_PATH = os.path.join(DB_DIR, "tasks.json")
    
    # Export Configuration
    EXPORT_DIR = os.path.join(BASE_DIR, "out")
    
    # Validation Constraints
    MAX_NAME_LENGTH = 64
    MAX_DESCRIPTION_LENGTH = 128
    MAX_DISPLAY_NAME_LENGTH = 64
    MAX_DISPLAY_NAME_UPDATE_LENGTH = 128
    MAX_TEAM_MEMBERS = 50
    
    # Status Constants
    BOARD_STATUS_OPEN = "OPEN"
    BOARD_STATUS_CLOSED = "CLOSED"
    
    TASK_STATUS_OPEN = "OPEN"
    TASK_STATUS_IN_PROGRESS = "IN_PROGRESS"
    TASK_STATUS_COMPLETE = "COMPLETE"
    
    VALID_TASK_STATUSES = [TASK_STATUS_OPEN, TASK_STATUS_IN_PROGRESS, TASK_STATUS_COMPLETE]
    VALID_BOARD_STATUSES = [BOARD_STATUS_OPEN, BOARD_STATUS_CLOSED]
    
    # Logging Configuration
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # API Configuration
    API_VERSION = "v1"
    API_TITLE = "Team Project Planner API"
    API_DESCRIPTION = "RESTful API for managing teams, projects, and tasks"

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    LOG_LEVEL = "DEBUG"

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    LOG_LEVEL = "WARNING"

class TestConfig(Config):
    """Test environment configuration."""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    # Use separate test database paths
    DB_DIR = os.path.join(BASE_DIR, "test_db")
    USERS_DB_PATH = os.path.join(DB_DIR, "users.json")
    TEAMS_DB_PATH = os.path.join(DB_DIR, "teams.json")
    BOARDS_DB_PATH = os.path.join(DB_DIR, "boards.json")
    TASKS_DB_PATH = os.path.join(DB_DIR, "tasks.json")

# Environment-based configuration selection
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}

def get_config(environment='default'):
    """Get configuration based on environment."""
    return config_map.get(environment, DevelopmentConfig)
