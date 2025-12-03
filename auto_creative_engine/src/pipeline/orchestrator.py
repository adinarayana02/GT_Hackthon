"""
Pipeline orchestrator for coordinating the generation workflow.
"""

from typing import Dict, Optional
from pathlib import Path

from .creative_engine import CreativeEngine
from ..config.settings import GenerationSettings
from ..utils.logger import get_logger

logger = get_logger()


class Orchestrator:
    """Orchestrates the complete creative generation workflow."""
    
    def __init__(self, settings: Optional[GenerationSettings] = None, api_key: Optional[str] = None):
        self.settings = settings or GenerationSettings()
        self.engine = CreativeEngine(self.settings, api_key)
        logger.info("Initialized Orchestrator")
    
    def run(
        self,
        product_description: str,
        logo_path: Optional[Path] = None,
        product_image_path: Optional[Path] = None,
        num_creatives: Optional[int] = None,
        brand_name: Optional[str] = None
    ) -> Dict:
        """Run the complete generation workflow."""
        logger.info("Starting orchestration...")
        
        # Update brand name if provided
        if brand_name:
            self.settings.brand_config.name = brand_name
        
        # Run generation
        results = self.engine.generate_creatives(
            product_description=product_description,
            logo_path=logo_path,
            product_image_path=product_image_path,
            num_creatives=num_creatives
        )
        
        logger.info("Orchestration completed successfully")
        return results

