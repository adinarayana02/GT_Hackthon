"""
Caption generator for creating ad captions.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path

from .llm_client import get_llm_client, LLMClient
from ..config.settings import LLMConfig, BrandConfig
from ..utils.logger import get_logger

logger = get_logger()


class CaptionGenerator:
    """Generates creative captions for ad creatives."""
    
    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        llm_config: Optional[LLMConfig] = None,
        brand_config: Optional[BrandConfig] = None
    ):
        self.llm_client = llm_client or get_llm_client(
            api_key=llm_config.api_key if llm_config else None,
            config=llm_config
        )
        self.brand_config = brand_config or BrandConfig()
        logger.info("Initialized CaptionGenerator")
    
    def generate_caption(
        self,
        image_description: str,
        product_description: Optional[str] = None,
        style: str = 'engaging',
        max_length: int = 150
    ) -> str:
        """Generate a single ad caption."""
        llm_prompt = f"""Generate a compelling social media ad caption for this creative.

Image Description: {image_description}
Product: {product_description or 'Not specified'}
Brand: {self.brand_config.name}
Brand Tone: {self.brand_config.tone}
Style: {style}

Requirements:
- Engaging and attention-grabbing
- Suitable for social media (Instagram, Facebook, Twitter)
- Include a call-to-action
- Match the brand tone: {self.brand_config.tone}
- Maximum {max_length} characters
- Use emojis sparingly (1-2 max)
- Be concise and impactful

Generate ONLY the caption text, nothing else:"""
        
        try:
            caption = self.llm_client.generate(
                llm_prompt,
                temperature=0.7,
                max_tokens=200
            )
            
            # Clean up and validate length
            caption = caption.strip()
            if caption.startswith('"') and caption.endswith('"'):
                caption = caption[1:-1]
            
            # Truncate if too long
            if len(caption) > max_length:
                caption = caption[:max_length-3] + "..."
            
            logger.debug(f"Generated caption ({len(caption)} chars)")
            return caption
        
        except Exception as e:
            logger.warning(f"LLM caption generation failed, using template: {e}")
            return self._get_fallback_caption(product_description or "product")
    
    def generate_multiple_captions(
        self,
        image_descriptions: List[str],
        product_description: Optional[str] = None,
        num_variations: int = 1
    ) -> Dict[str, List[str]]:
        """Generate multiple caption variations for each image."""
        results = {}
        
        for i, desc in enumerate(image_descriptions):
            variations = []
            for j in range(num_variations):
                style = ['engaging', 'professional', 'playful', 'bold'][j % 4]
                caption = self.generate_caption(
                    desc,
                    product_description,
                    style=style
                )
                variations.append(caption)
            
            results[f"image_{i+1}"] = variations
        
        logger.info(f"Generated captions for {len(image_descriptions)} images")
        return results
    
    def _get_fallback_caption(self, product_description: str) -> str:
        """Generate a fallback caption if LLM fails."""
        templates = [
            f"Discover {product_description}! ✨ Perfect for your lifestyle. Shop now!",
            f"Elevate your experience with {product_description}. Limited time offer!",
            f"{product_description} - Quality you can trust. Order today!",
            f"Transform your day with {product_description}. Get yours now!",
        ]
        
        import random
        return random.choice(templates)

