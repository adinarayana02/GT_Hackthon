from pathlib import Path
from typing import Tuple, Optional
from PIL import Image, ImageEnhance

from ..utils.logger import get_logger

logger = get_logger()


def enhance_image(
    image_path: Path,
    output_path: Path,
    brightness: float = 1.0,
    contrast: float = 1.0,
    saturation: float = 1.0,
    sharpness: float = 1.0
) -> Path:
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Apply enhancements
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)
            
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)
            
            if saturation != 1.0:
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(saturation)
            
            if sharpness != 1.0:
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(sharpness)
            
            img.save(output_path, 'JPEG', quality=95)
            logger.debug(f"Enhanced image saved to {output_path}")
            return output_path
    
    except Exception as e:
        logger.error(f"Error enhancing image: {e}")
        raise


def apply_brand_colors(
    image_path: Path,
    output_path: Path,
    brand_colors: list,
    intensity: float = 0.3
) -> Path:
    try:
        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Create a color overlay based on brand colors
            if brand_colors:
                # Use the first brand color as overlay
                color_hex = brand_colors[0].replace('#', '')
                r = int(color_hex[0:2], 16)
                g = int(color_hex[2:4], 16)
                b = int(color_hex[4:6], 16)
                
                overlay = Image.new('RGB', img.size, (r, g, b))
                img = Image.blend(img, overlay, intensity)
            
            img.save(output_path, 'JPEG', quality=95)
            logger.debug(f"Applied brand colors to {output_path}")
            return output_path
    
    except Exception as e:
        logger.error(f"Error applying brand colors: {e}")
        raise


def validate_image_quality(image_path: Path) -> bool:
    try:
        with Image.open(image_path) as img:
            # Check dimensions
            width, height = img.size
            if width < 512 or height < 512:
                logger.warning(f"Image dimensions too small: {width}x{height}")
                return False
            
            # Check file size
            file_size = image_path.stat().st_size
            if file_size < 10000:  # Less than 10KB
                logger.warning(f"Image file too small: {file_size} bytes")
                return False
            
            return True
    
    except Exception as e:
        logger.error(f"Error validating image quality: {e}")
        return False

