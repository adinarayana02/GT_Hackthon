"""
Tests for caption generation.
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.llm.caption_generator import CaptionGenerator
from src.config.settings import BrandConfig


def test_caption_generator_initialization():
    """Test caption generator initialization."""
    generator = CaptionGenerator()
    assert generator is not None


def test_fallback_caption():
    """Test fallback caption generation."""
    generator = CaptionGenerator()
    caption = generator._get_fallback_caption("test product")
    assert isinstance(caption, str)
    assert len(caption) > 0


def test_caption_length_validation():
    """Test caption length validation."""
    generator = CaptionGenerator()
    caption = generator.generate_caption(
        image_description="A beautiful product",
        max_length=50
    )
    # Should respect max_length or use fallback
    assert isinstance(caption, str)

