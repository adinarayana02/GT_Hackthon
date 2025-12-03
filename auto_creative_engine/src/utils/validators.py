"""
Validation utilities for inputs and data.
"""

from pathlib import Path
from typing import Optional, List
from PIL import Image

from .logger import get_logger

logger = get_logger()


class ValidationError(Exception):
    """Custom validation error."""
    pass


def validate_image_path(image_path: Path, required: bool = True) -> bool:
    """Validate that an image path exists and is a valid image."""
    if not image_path:
        if required:
            raise ValidationError("Image path is required")
        return False
    
    if not isinstance(image_path, Path):
        image_path = Path(image_path)
    
    if not image_path.exists():
        raise ValidationError(f"Image file does not exist: {image_path}")
    
    if not image_path.is_file():
        raise ValidationError(f"Path is not a file: {image_path}")
    
    # Check if it's a valid image
    try:
        with Image.open(image_path) as img:
            img.verify()
        
        # Check file size (max 10MB)
        size_mb = image_path.stat().st_size / (1024 * 1024)
        if size_mb > 10:
            raise ValidationError(f"Image file too large: {size_mb:.2f}MB (max 10MB)")
        
        return True
    except Exception as e:
        raise ValidationError(f"Invalid image file: {e}")


def validate_output_dir(output_dir: Path) -> Path:
    """Validate and create output directory if needed."""
    if not output_dir:
        raise ValidationError("Output directory is required")
    
    if not isinstance(output_dir, Path):
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def validate_api_key(api_key: Optional[str], service_name: str) -> str:
    """Validate that an API key is provided."""
    if not api_key or not api_key.strip():
        raise ValidationError(f"{service_name} API key is required")
    return api_key.strip()


def validate_count(count: int, min_val: int = 1, max_val: int = 50) -> int:
    """Validate a count value."""
    if not isinstance(count, int):
        raise ValidationError("Count must be an integer")
    
    if count < min_val:
        raise ValidationError(f"Count must be at least {min_val}")
    
    if count > max_val:
        raise ValidationError(f"Count must be at most {max_val}")
    
    return count


def validate_brand_name(brand_name: Optional[str]) -> str:
    """Validate brand name."""
    if not brand_name or not brand_name.strip():
        return "Brand"
    
    name = brand_name.strip()
    if len(name) > 100:
        name = name[:100]
    
    return name

