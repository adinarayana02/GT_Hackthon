"""
Prompt generator for creating image generation prompts.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path

from .llm_client import get_llm_client, LLMClient
from ..config.settings import LLMConfig, BrandConfig
from ..config.constants import PROMPT_STYLES
from ..utils.logger import get_logger

logger = get_logger()


class PromptGenerator:
    """Generates creative prompts for image generation."""
    
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
        logger.info("Initialized PromptGenerator")
    
    def generate_image_prompts(
        self,
        product_description: str,
        num_prompts: int = 10,
        style_variations: Optional[List[str]] = None
    ) -> List[str]:
        """Generate multiple creative image prompts."""
        style_variations = style_variations or PROMPT_STYLES[:num_prompts]
        
        prompts = []
        base_prompt_template = self._get_base_prompt_template()
        
        for i in range(num_prompts):
            style = style_variations[i % len(style_variations)]
            prompt = self._generate_single_prompt(
                product_description,
                style,
                base_prompt_template
            )
            prompts.append(prompt)
        
        logger.info(f"Generated {len(prompts)} image prompts")
        return prompts
    
    def _generate_single_prompt(
        self,
        product_description: str,
        style: str,
        base_template: str
    ) -> str:
        """Generate a single creative prompt using LLM."""
        llm_prompt = f"""Generate a creative, detailed image generation prompt for an advertisement.

Product Description: {product_description}
Style: {style}
Brand Name: {self.brand_config.name}
Brand Theme: {self.brand_config.theme}
Brand Tone: {self.brand_config.tone}
Brand Colors: {', '.join(self.brand_config.colors) if self.brand_config.colors else 'Not specified'}

Requirements:
- Create a compelling, visually striking ad creative
- Include the product naturally in the scene
- Use the specified style and theme
- Make it suitable for social media advertising
- Be specific about composition, lighting, mood, and colors
- Keep the prompt under 200 words
- Do NOT include any text or words in the image description

Generate ONLY the image prompt, nothing else:"""
        
        try:
            generated_prompt = self.llm_client.generate(
                llm_prompt,
                temperature=0.8,
                max_tokens=300
            )
            
            # Clean up the response
            generated_prompt = generated_prompt.strip()
            if generated_prompt.startswith('"') and generated_prompt.endswith('"'):
                generated_prompt = generated_prompt[1:-1]
            
            return generated_prompt
        
        except Exception as e:
            logger.warning(f"LLM prompt generation failed, using template: {e}")
            return self._get_fallback_prompt(product_description, style)
    
    def _get_base_prompt_template(self) -> str:
        """Get base prompt template."""
        return """Create a professional advertisement image featuring {product} in a {style} style. 
        The image should convey {tone} and align with {theme} theme. 
        Use brand colors: {colors}. 
        Composition should be eye-catching and suitable for social media marketing."""
    
    def _get_fallback_prompt(
        self,
        product_description: str,
        style: str
    ) -> str:
        """Generate a fallback prompt if LLM fails."""
        colors_text = f" with brand colors {', '.join(self.brand_config.colors)}" if self.brand_config.colors else ""
        
        return f"""Professional advertisement image featuring {product_description} in {style} style{colors_text}. 
        {self.brand_config.theme} theme, {self.brand_config.tone} tone. 
        Eye-catching composition, high quality, suitable for social media marketing, 
        clean background, professional lighting, vibrant colors, modern design."""
    
    def enhance_prompt_with_brand(
        self,
        base_prompt: str,
        brand_logo_path: Optional[Path] = None
    ) -> str:
        """Enhance a prompt with brand-specific details."""
        enhancements = []
        
        if self.brand_config.colors:
            enhancements.append(f"Brand colors: {', '.join(self.brand_config.colors)}")
        
        if self.brand_config.theme:
            enhancements.append(f"Theme: {self.brand_config.theme}")
        
        if self.brand_config.tone:
            enhancements.append(f"Tone: {self.brand_config.tone}")
        
        if enhancements:
            enhanced = f"{base_prompt}\n\nBrand guidelines: {', '.join(enhancements)}"
            return enhanced
        
        return base_prompt

