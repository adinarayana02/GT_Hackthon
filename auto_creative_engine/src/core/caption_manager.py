"""
Caption manager for handling caption generation and storage.
"""

from typing import List, Dict, Optional
from pathlib import Path

from ..llm.caption_generator import CaptionGenerator
from ..config.settings import GenerationSettings
from ..utils.logger import get_logger
from ..utils.json_utils import save_json
from ..utils.file_utils import ensure_dir

logger = get_logger()


class CaptionManager:
    """Manages caption generation and storage."""
    
    def __init__(self, settings: GenerationSettings):
        self.settings = settings
        self.caption_generator = CaptionGenerator(
            llm_config=settings.llm_config,
            brand_config=settings.brand_config
        )
        logger.info("Initialized CaptionManager")
    
    def generate_captions(
        self,
        image_paths: List[Path],
        image_descriptions: List[str],
        product_description: Optional[str] = None
    ) -> Dict[str, str]:
        """Generate captions for images."""
        captions = {}
        
        for i, (image_path, description) in enumerate(zip(image_paths, image_descriptions)):
            try:
                caption = self.caption_generator.generate_caption(
                    image_description=description,
                    product_description=product_description
                )
                
                image_name = image_path.stem
                captions[image_name] = caption
                
                logger.debug(f"Generated caption for {image_name}")
            
            except Exception as e:
                logger.error(f"Error generating caption for {image_path}: {e}")
                captions[image_path.stem] = "Check out our amazing product!"
        
        logger.info(f"Generated {len(captions)} captions")
        return captions
    
    def save_captions(
        self,
        captions: Dict[str, str],
        output_dir: Path
    ) -> Dict[str, Path]:
        """Save captions to individual files and return mapping."""
        ensure_dir(output_dir)
        saved_paths = {}
        
        for image_name, caption in captions.items():
            caption_path = output_dir / f"{image_name}.txt"
            caption_path.write_text(caption, encoding='utf-8')
            saved_paths[image_name] = caption_path
        
        logger.info(f"Saved {len(saved_paths)} caption files")
        return saved_paths
    
    def save_caption_mapping(
        self,
        captions: Dict[str, str],
        output_path: Path
    ) -> Path:
        """Save caption mapping to JSON."""
        mapping = {
            "mapping": captions,
            "count": len(captions)
        }
        return save_json(mapping, output_path)

