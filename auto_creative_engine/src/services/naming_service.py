"""
Naming service for generating consistent file names.
"""

from typing import Optional
from pathlib import Path
from datetime import datetime

from ..config.constants import TIMESTAMP_FORMAT, CREATIVE_PREFIX, CAPTION_PREFIX
from ..utils.logger import get_logger

logger = get_logger()


class NamingService:
    """Generates consistent file names for outputs."""
    
    def __init__(self, prefix: str = CREATIVE_PREFIX):
        self.prefix = prefix
        logger.info("Initialized NamingService")
    
    def generate_image_name(
        self,
        index: int,
        extension: str = '.jpg',
        timestamp: bool = False
    ) -> str:
        """Generate a name for an image file."""
        if timestamp:
            ts = datetime.now().strftime(TIMESTAMP_FORMAT)
            return f"{self.prefix}_{ts}_{index:03d}{extension}"
        else:
            return f"{self.prefix}_{index:03d}{extension}"
    
    def generate_caption_name(
        self,
        image_name: str,
        extension: str = '.txt'
    ) -> str:
        """Generate a caption file name matching an image."""
        base_name = Path(image_name).stem
        return f"{base_name}{extension}"
    
    def generate_zip_name(
        self,
        brand_name: Optional[str] = None,
        timestamp: bool = True
    ) -> str:
        """Generate a name for the output ZIP file."""
        if timestamp:
            ts = datetime.now().strftime(TIMESTAMP_FORMAT)
            if brand_name:
                return f"{brand_name}_creatives_{ts}.zip"
            return f"creatives_{ts}.zip"
        else:
            if brand_name:
                return f"{brand_name}_creatives.zip"
            return "creatives.zip"

