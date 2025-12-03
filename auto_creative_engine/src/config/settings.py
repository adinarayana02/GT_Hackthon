"""
Application settings and configuration.
"""

from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

from .constants import (
    BASE_DIR, DATA_DIR, INPUT_DIR, OUTPUT_DIR, TEMP_DIR,
    IMAGES_DIR, CAPTIONS_DIR, DEFAULT_NUM_CREATIVES,
    DEFAULT_IMAGE_SIZE
)
from .env import (
    GEMINI_API_KEY,
    DEFAULT_LLM_PROVIDER, DEFAULT_IMAGE_MODEL
)
from ..utils.logger import get_logger

logger = get_logger()


@dataclass
class ImageGenConfig:
    """Image generation configuration."""
    model: str = 'imagen3'
    aspect_ratio: str = '1:1'
    num_images: int = 1
    api_key: Optional[str] = None


@dataclass
class LLMConfig:
    """LLM configuration."""
    provider: str = 'gemini'
    model: str = 'gemini-1.5-flash'
    temperature: float = 0.7
    max_tokens: int = 1000
    timeout: int = 60
    api_key: Optional[str] = None


@dataclass
class BrandConfig:
    """Brand configuration."""
    name: str = 'Brand'
    colors: list = field(default_factory=list)
    theme: str = 'modern'
    tone: str = 'professional'
    style_preferences: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerationSettings:
    """Complete generation settings."""
    num_creatives: int = DEFAULT_NUM_CREATIVES
    image_config: ImageGenConfig = field(default_factory=ImageGenConfig)
    llm_config: LLMConfig = field(default_factory=LLMConfig)
    brand_config: BrandConfig = field(default_factory=BrandConfig)
    output_dir: Path = OUTPUT_DIR
    use_brand_colors: bool = True
    use_themes: bool = True
    generate_captions: bool = True
    
    def __post_init__(self):
        """Validate and set defaults after initialization."""
        # Ensure output directories exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        CAPTIONS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Set API keys
        if GEMINI_API_KEY:
            self.llm_config.api_key = GEMINI_API_KEY
            self.image_config.api_key = GEMINI_API_KEY


def get_default_settings() -> GenerationSettings:
    """Get default generation settings."""
    return GenerationSettings()
