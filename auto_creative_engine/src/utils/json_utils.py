"""
JSON utility functions for handling JSON operations.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from .logger import get_logger

logger = get_logger()


def save_json(data: Dict[str, Any], file_path: Path, indent: int = 2) -> Path:
    """Save data to a JSON file."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        
        logger.debug(f"Saved JSON to {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error saving JSON to {file_path}: {e}")
        raise


def load_json(file_path: Path) -> Dict[str, Any]:
    """Load data from a JSON file."""
    try:
        if not file_path.exists():
            logger.warning(f"JSON file does not exist: {file_path}")
            return {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.debug(f"Loaded JSON from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading JSON from {file_path}: {e}")
        raise


def update_json(file_path: Path, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update a JSON file with new data."""
    existing_data = load_json(file_path)
    existing_data.update(updates)
    save_json(existing_data, file_path)
    return existing_data

