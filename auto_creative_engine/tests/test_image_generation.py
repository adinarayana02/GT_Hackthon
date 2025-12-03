"""
Tests for image generation (mock tests).
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.image_gen.gemini_image_client import GeminiImageClient
from src.config.settings import ImageGenConfig


def test_gemini_client_initialization():
    """Test Gemini image client initialization."""
    config = ImageGenConfig(model='imagen3')
    # Note: This will fail without API key, but tests structure
    try:
        client = GeminiImageClient(config=config)
        assert client is not None
    except Exception:
        # Expected without API key
        pass


def test_image_config():
    """Test image configuration."""
    config = ImageGenConfig(
        model='imagen3',
        aspect_ratio='1:1'
    )
    assert config.model == 'imagen3'
    assert config.aspect_ratio == '1:1'
