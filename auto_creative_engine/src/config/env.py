"""
Environment variable management.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from .constants import BASE_DIR

# Load .env file if it exists
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)


class EnvConfig:
    """Environment configuration manager."""
    
    @staticmethod
    def get(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
        """Get an environment variable."""
        value = os.getenv(key, default)
        
        if required and not value:
            raise ValueError(f"Required environment variable {key} is not set")
        
        return value
    
    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        """Get a boolean environment variable."""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    @staticmethod
    def get_int(key: str, default: int = 0) -> int:
        """Get an integer environment variable."""
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            return default
    
    @staticmethod
    def get_float(key: str, default: float = 0.0) -> float:
        """Get a float environment variable."""
        try:
            return float(os.getenv(key, str(default)))
        except ValueError:
            return default


# API Keys
GEMINI_API_KEY = EnvConfig.get('GEMINI_API_KEY', required=False)

# Model preferences
DEFAULT_LLM_PROVIDER = EnvConfig.get('DEFAULT_LLM_PROVIDER', 'gemini')
DEFAULT_IMAGE_MODEL = EnvConfig.get('DEFAULT_IMAGE_MODEL', 'imagen3')

# Generation settings
DEFAULT_NUM_CREATIVES = EnvConfig.get_int('DEFAULT_NUM_CREATIVES', 10)
MAX_IMAGE_SIZE = EnvConfig.get_int('MAX_IMAGE_SIZE', 2048)

# Logging
LOG_LEVEL = EnvConfig.get('LOG_LEVEL', 'INFO')
