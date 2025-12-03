from typing import List, Dict, Optional
from pathlib import Path

from ..core.prompt_manager import PromptManager
from ..core.caption_manager import CaptionManager
from ..core.image_manager import ImageManager
from ..image_gen.image_pipeline import ImageGenerationPipeline
from ..services.brand_color_extractor import BrandColorExtractor
from ..services.theme_service import ThemeService
from ..config.settings import GenerationSettings, BrandConfig
from ..utils.logger import get_logger
from ..utils.validators import validate_image_path

logger = get_logger()


class CreativeEngine:
    """Main engine for generating ad creatives."""
    
    def __init__(self, settings: Optional[GenerationSettings] = None, api_key: Optional[str] = None):
        self.settings = settings or GenerationSettings()
        self.api_key = api_key
        
        # Initialize components
        self.prompt_manager = PromptManager(self.settings)
        self.caption_manager = CaptionManager(self.settings)
        self.image_manager = ImageManager(self.settings)
        self.image_pipeline = ImageGenerationPipeline(self.settings, self.api_key)
        self.color_extractor = BrandColorExtractor()
        self.theme_service = ThemeService()
        
        logger.info("Initialized CreativeEngine")
    
    def process_brand_inputs(
        self,
        logo_path: Optional[Path] = None,
        product_path: Optional[Path] = None
    ) -> BrandConfig:
        """Process brand inputs and extract information."""
        brand_config = self.settings.brand_config
        
        # Extract colors from logo if provided
        if logo_path and self.settings.use_brand_colors:
            try:
                validate_image_path(logo_path)
                colors = self.color_extractor.extract_colors(logo_path)
                brand_config.colors = colors
                logger.info(f"Extracted {len(colors)} brand colors")
            except Exception as e:
                logger.warning(f"Could not extract brand colors: {e}")
        
        return brand_config
    
    def generate_creatives(
        self,
        product_description: str,
        logo_path: Optional[Path] = None,
        product_image_path: Optional[Path] = None,
        num_creatives: Optional[int] = None
    ) -> Dict[str, any]:
        """Generate complete set of ad creatives."""
        logger.info("Starting creative generation pipeline...")
        
        # Process brand inputs
        brand_config = self.process_brand_inputs(logo_path, product_image_path)
        self.settings.brand_config = brand_config
        
        # Update prompt and caption generators with brand config
        self.prompt_manager.prompt_generator.brand_config = brand_config
        self.caption_manager.caption_generator.brand_config = brand_config
        
        # Generate prompts
        num_creatives = num_creatives or self.settings.num_creatives
        prompts = self.prompt_manager.generate_prompts(
            product_description,
            num_prompts=num_creatives
        )
        
        # Generate images
        images_dir = self.settings.output_dir / 'images'
        self.image_manager.prepare_output_directory(self.settings.output_dir)
        
        image_paths = self.image_pipeline.generate_creatives(
            prompts=prompts,
            output_dir=images_dir,
            product_image_path=product_image_path
        )
        
        # Generate captions
        image_descriptions = prompts  # Use prompts as descriptions
        captions = self.caption_manager.generate_captions(
            image_paths=image_paths,
            image_descriptions=image_descriptions,
            product_description=product_description
        )
        
        # Save captions
        captions_dir = self.settings.output_dir / 'captions'
        self.caption_manager.save_captions(captions, captions_dir)
        
        # Save mapping
        mapping_path = self.settings.output_dir / 'mapping.json'
        self.caption_manager.save_caption_mapping(captions, mapping_path)
        
        logger.info(f"Successfully generated {len(image_paths)} creatives")
        
        return {
            "images": image_paths,
            "captions": captions,
            "prompts": prompts,
            "mapping_path": mapping_path,
            "count": len(image_paths)
        }

