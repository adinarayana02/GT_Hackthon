"""
ZIP packager for creating downloadable output packages.
"""

import zipfile
from pathlib import Path
from typing import List, Dict, Optional

from ..config.constants import ZIP_FILENAME, MAX_ZIP_SIZE_MB
from ..services.naming_service import NamingService
from ..utils.logger import get_logger
from ..utils.file_utils import ensure_dir

logger = get_logger()


class Packager:
    """Packages generated creatives into ZIP files."""
    
    def __init__(self):
        self.naming_service = NamingService()
        logger.info("Initialized Packager")
    
    def create_zip(
        self,
        images_dir: Path,
        captions_dir: Path,
        mapping_path: Path,
        output_path: Optional[Path] = None,
        brand_name: Optional[str] = None
    ) -> Path:
        """Create a ZIP file containing all creatives."""
        if output_path is None:
            output_dir = images_dir.parent
            output_path = output_dir / self.naming_service.generate_zip_name(brand_name)
        
        ensure_dir(output_path.parent)
        
        logger.info(f"Creating ZIP package: {output_path}")
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add images
            image_files = sorted(images_dir.glob('*.jpg'))
            for img_file in image_files:
                zipf.write(img_file, f"images/{img_file.name}")
                logger.debug(f"Added image: {img_file.name}")
            
            # Add captions
            caption_files = sorted(captions_dir.glob('*.txt'))
            for cap_file in caption_files:
                zipf.write(cap_file, f"captions/{cap_file.name}")
                logger.debug(f"Added caption: {cap_file.name}")
            
            # Add mapping JSON
            if mapping_path.exists():
                zipf.write(mapping_path, "mapping.json")
                logger.debug("Added mapping.json")
        
        # Check file size
        zip_size_mb = output_path.stat().st_size / (1024 * 1024)
        logger.info(f"ZIP created: {output_path} ({zip_size_mb:.2f} MB)")
        
        if zip_size_mb > MAX_ZIP_SIZE_MB:
            logger.warning(f"ZIP file exceeds recommended size: {zip_size_mb:.2f} MB")
        
        return output_path
    
    def create_zip_from_results(
        self,
        results: Dict,
        output_dir: Path,
        brand_name: Optional[str] = None
    ) -> Path:
        """Create ZIP from generation results."""
        images_dir = output_dir / 'images'
        captions_dir = output_dir / 'captions'
        mapping_path = output_dir / 'mapping.json'
        
        return self.create_zip(
            images_dir=images_dir,
            captions_dir=captions_dir,
            mapping_path=mapping_path,
            output_path=output_dir / ZIP_FILENAME,
            brand_name=brand_name
        )

