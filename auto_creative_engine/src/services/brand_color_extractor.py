"""
Brand color extraction from logo images.
"""

from typing import List, Tuple
from pathlib import Path
from collections import Counter

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

from ..config.constants import DEFAULT_COLOR_COUNT
from ..utils.logger import get_logger

logger = get_logger()


class BrandColorExtractor:
    """Extracts dominant colors from brand logo."""
    
    def __init__(self, num_colors: int = DEFAULT_COLOR_COUNT):
        self.num_colors = num_colors
        logger.info(f"Initialized BrandColorExtractor (colors: {num_colors})")
    
    def extract_colors(self, image_path: Path) -> List[str]:
        """Extract dominant colors from an image."""
        try:
            with Image.open(image_path) as img:
                # Resize for faster processing
                img = img.resize((200, 200))
                
                # Convert to RGB
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Convert to numpy array
                img_array = np.array(img)
                pixels = img_array.reshape(-1, 3)
                
                # Remove white/black pixels (background)
                pixels = pixels[
                    (pixels.sum(axis=1) > 30) &  # Not too dark
                    (pixels.sum(axis=1) < 750)    # Not too light
                ]
                
                if len(pixels) == 0:
                    pixels = img_array.reshape(-1, 3)
                
                # Use KMeans to find dominant colors
                kmeans = KMeans(n_clusters=self.num_colors, random_state=42, n_init=10)
                kmeans.fit(pixels)
                
                # Get cluster centers (colors)
                colors = kmeans.cluster_centers_.astype(int)
                
                # Convert to hex
                hex_colors = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in colors]
                
                logger.info(f"Extracted {len(hex_colors)} brand colors")
                return hex_colors
        
        except Exception as e:
            logger.warning(f"Error extracting colors, using defaults: {e}")
            return self._get_default_colors()
    
    def _get_default_colors(self) -> List[str]:
        """Return default brand colors if extraction fails."""
        return ["#1a1a1a", "#4a90e2", "#50c878", "#ff6b6b", "#ffd93d"]

