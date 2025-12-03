"""
Tests for ZIP packager.
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline.packager import Packager


def test_packager_initialization():
    """Test packager initialization."""
    packager = Packager()
    assert packager is not None


def test_zip_name_generation():
    """Test ZIP name generation."""
    packager = Packager()
    name = packager.naming_service.generate_zip_name(brand_name="TestBrand")
    assert "TestBrand" in name
    assert name.endswith(".zip")


def test_image_name_generation():
    """Test image name generation."""
    packager = Packager()
    name = packager.naming_service.generate_image_name(index=1)
    assert "creative" in name.lower()
    assert name.endswith(".jpg")

