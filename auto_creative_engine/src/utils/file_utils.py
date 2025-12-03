"""
File utility functions for handling file operations.
"""

import shutil
from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image
import mimetypes

from .logger import get_logger

logger = get_logger()


def ensure_dir(directory: Path) -> Path:
    """Ensure a directory exists, create if it doesn't."""
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def clean_dir(directory: Path, pattern: Optional[str] = None) -> None:
    """Clean all files in a directory."""
    if not directory.exists():
        return
    
    for item in directory.iterdir():
        if item.is_file():
            if pattern is None or pattern in item.name:
                item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)


def get_file_size(file_path: Path) -> int:
    """Get file size in bytes."""
    return file_path.stat().st_size if file_path.exists() else 0


def is_valid_image(file_path: Path) -> bool:
    """Check if file is a valid image."""
    try:
        if not file_path.exists():
            return False
        
        # Check MIME type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type and not mime_type.startswith('image/'):
            return False
        
        # Try to open with PIL
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception as e:
        logger.warning(f"Invalid image file {file_path}: {e}")
        return False


def resize_image(
    image_path: Path,
    output_path: Path,
    max_size: Tuple[int, int] = (2048, 2048),
    quality: int = 95
) -> Path:
    """Resize an image while maintaining aspect ratio."""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            logger.info(f"Resized image: {image_path.name} -> {output_path.name}")
            return output_path
    except Exception as e:
        logger.error(f"Error resizing image {image_path}: {e}")
        raise


def copy_file(source: Path, destination: Path) -> Path:
    """Copy a file from source to destination."""
    ensure_dir(destination.parent)
    shutil.copy2(source, destination)
    return destination


def get_image_dimensions(image_path: Path) -> Tuple[int, int]:
    """Get image dimensions (width, height)."""
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        logger.error(f"Error getting dimensions for {image_path}: {e}")
        return (0, 0)


def list_files(directory: Path, extension: Optional[str] = None) -> List[Path]:
    """List all files in a directory, optionally filtered by extension."""
    if not directory.exists():
        return []
    
    files = [f for f in directory.iterdir() if f.is_file()]
    
    if extension:
        files = [f for f in files if f.suffix.lower() == extension.lower()]
    
    return sorted(files)

