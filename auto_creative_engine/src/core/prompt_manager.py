"""
Prompt manager for handling prompt generation and storage.
"""

from typing import List, Dict
from pathlib import Path

from ..llm.prompt_generator import PromptGenerator
from ..config.settings import GenerationSettings, BrandConfig
from ..utils.logger import get_logger
from ..utils.json_utils import save_json, load_json

logger = get_logger()


class PromptManager:
    """Manages prompt generation and storage."""
    
    def __init__(self, settings: GenerationSettings):
        self.settings = settings
        self.prompt_generator = PromptGenerator(
            llm_config=settings.llm_config,
            brand_config=settings.brand_config
        )
        logger.info("Initialized PromptManager")
    
    def generate_prompts(
        self,
        product_description: str,
        num_prompts: Optional[int] = None
    ) -> List[str]:
        """Generate creative prompts for image generation."""
        num_prompts = num_prompts or self.settings.num_creatives
        
        prompts = self.prompt_generator.generate_image_prompts(
            product_description=product_description,
            num_prompts=num_prompts
        )
        
        logger.info(f"Generated {len(prompts)} prompts")
        return prompts
    
    def save_prompts(self, prompts: List[str], output_path: Path) -> Path:
        """Save prompts to a JSON file."""
        data = {
            "prompts": prompts,
            "count": len(prompts),
            "brand": self.settings.brand_config.name
        }
        return save_json(data, output_path)
    
    def load_prompts(self, input_path: Path) -> List[str]:
        """Load prompts from a JSON file."""
        data = load_json(input_path)
        return data.get("prompts", [])

