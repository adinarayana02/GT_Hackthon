"""
Logging utility for the Auto-Creative Engine.
Provides centralized logging configuration.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class Logger:
    """Centralized logger for the application."""
    
    _instance: Optional['Logger'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.logger = logging.getLogger('auto_creative_engine')
            self.logger.setLevel(logging.DEBUG)
            
            # Prevent duplicate handlers
            if not self.logger.handlers:
                self._setup_handlers()
            
            Logger._initialized = True
    
    def _setup_handlers(self):
        """Configure logging handlers."""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        
        # File handler
        log_dir = Path(__file__).parent.parent.parent / 'data' / 'temp'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f'creative_engine_{datetime.now().strftime("%Y%m%d")}.log'
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def get_logger(self) -> logging.Logger:
        """Get the logger instance."""
        return self.logger


def get_logger() -> logging.Logger:
    """Get the application logger."""
    return Logger().get_logger()

