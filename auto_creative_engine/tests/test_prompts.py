"""
Tests for prompt generation.
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.llm.prompt_generator import PromptGenerator
from src.config.settings import LLMConfig, BrandConfig


def test_prompt_generator_initialization():
    """Test prompt generator initialization."""
    generator = PromptGenerator()
    assert generator is not None


def test_prompt_generation_without_llm():
    """Test fallback prompt generation."""
    generator = PromptGenerator()
    prompts = generator.generate_image_prompts(
        product_description="A premium wireless headphone",
        num_prompts=3
    )
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


def test_brand_config_integration():
    """Test brand config integration."""
    brand_config = BrandConfig(
        name="TestBrand",
        colors=["#FF0000", "#00FF00"],
        theme="modern"
    )
    generator = PromptGenerator(brand_config=brand_config)
    assert generator.brand_config.name == "TestBrand"

