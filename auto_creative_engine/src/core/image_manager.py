"""
Image manager for handling image operations.
"""

from typing import List, Optional, Tuple
from pathlib import Path

from ..config.settings import GenerationSettings
from ..utils.logger import get_logger
from ..utils.file_utils import (
    ensure_dir, list_files, is_valid_image,
    resize_image, get_image_dimensions
)

logger = get_logger()


class ImageManager:
    """Manages image operations and validation."""
    
    def __init__(self, settings: GenerationSettings):
        self.settings = settings
        logger.info("Initialized ImageManager")
    
    def validate_input_images(
        self,
        logo_path: Optional[Path] = None,
        product_path: Optional[Path] = None
    ) -> tuple[bool, Optional[str]]:
        """Validate input images."""
        if logo_path and not is_valid_image(logo_path):
            return False, f"Invalid logo image: {logo_path}"
        
        if product_path and not is_valid_image(product_path):
            return False, f"Invalid product image: {product_path}"
        
        return True, None
    
    def prepare_output_directory(self, output_dir: Path) -> Path:
        """Prepare output directory structure."""
        images_dir = output_dir / 'images'
        captions_dir = output_dir / 'captions'
        
        ensure_dir(images_dir)
        ensure_dir(captions_dir)
        
        return images_dir
    
    def list_generated_images(self, images_dir: Path) -> List[Path]:
        """List all generated images."""
        return list_files(images_dir, extension='.jpg')
    
    def get_image_info(self, image_path: Path) -> dict:
        """Get information about an image."""
        dimensions = get_image_dimensions(image_path)
        size = image_path.stat().st_size
        
        return {
            "path": str(image_path),
            "name": image_path.name,
            "dimensions": dimensions,
            "size_bytes": size,
            "size_mb": round(size / (1024 * 1024), 2)
        }

