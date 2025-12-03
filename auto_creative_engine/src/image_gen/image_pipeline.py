from typing import List, Optional
from pathlib import Path

from .sdxl_pipeline import SDXLPipeline
from ..config.settings import GenerationSettings
from ..utils.logger import get_logger
from ..utils.file_utils import ensure_dir

logger = get_logger()


class ImageGenerationPipeline:
    """Orchestrates the image generation process."""
    
    def __init__(
        self,
        settings: Optional[GenerationSettings] = None,
        api_key: Optional[str] = None
    ):
        self.settings = settings or GenerationSettings()
        self.api_key = api_key
        
        # Initialize Gemini Imagen client
        self.image_client = SDXLPipeline(
            config=self.settings.image_config
        )
        
        logger.info("Initialized ImageGenerationPipeline")
    
    def generate_creatives(
        self,
        prompts: List[str],
        output_dir: Optional[Path] = None,
        product_image_path: Optional[Path] = None
    ) -> List[Path]:
        """Generate creative images from prompts."""
        output_dir = output_dir or self.settings.output_dir / 'images'
        ensure_dir(output_dir)
        
        logger.info(f"Generating {len(prompts)} creatives...")
        
        generated_images = self.image_client.generate_images(
            prompts=prompts,
            output_dir=output_dir,
            aspect_ratio="1:1",
            product_image_path=product_image_path
        )
        
        logger.info(f"Successfully generated {len(generated_images)} creatives")
        return generated_images
    
    def generate_single_creative(
        self,
        prompt: str,
        output_path: Optional[Path] = None
    ) -> Path:
        """Generate a single creative image."""
        if output_path is None:
            output_dir = self.settings.output_dir / 'images'
            ensure_dir(output_dir)
            output_path = output_dir / f"creative_{len(list(output_dir.glob('*.jpg')))+1:03d}.jpg"
        
        logger.info(f"Generating single creative: {prompt[:50]}...")
        
        image_path = self.image_client.generate_image(
            prompt=prompt,
            aspect_ratio="1:1",
            output_path=output_path
        )
        
        return image_path
