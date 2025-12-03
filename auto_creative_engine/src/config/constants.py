"""
Constants used throughout the application.
"""

from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
INPUT_DIR = DATA_DIR / 'input'
OUTPUT_DIR = DATA_DIR / 'outputs'
TEMP_DIR = DATA_DIR / 'temp'
IMAGES_DIR = OUTPUT_DIR / 'images'
CAPTIONS_DIR = OUTPUT_DIR / 'captions'

# Image generation settings
DEFAULT_NUM_CREATIVES = 10
MAX_NUM_CREATIVES = 50
MIN_NUM_CREATIVES = 1

# Image dimensions
DEFAULT_IMAGE_SIZE = (1024, 1024)
IMAGEN_ASPECT_RATIOS = ['1:1', '16:9', '9:16', '4:3', '3:4']

# Supported image formats
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']
OUTPUT_IMAGE_FORMAT = 'jpg'
OUTPUT_IMAGE_QUALITY = 95

# API settings
GEMINI_MAX_RETRIES = 3
GEMINI_TIMEOUT = 120

# Brand color extraction
DEFAULT_COLOR_COUNT = 5
COLOR_EXTRACTION_METHOD = 'kmeans'

# Theme variations
THEMES = [
    'modern',
    'minimalist',
    'luxury',
    'playful',
    'professional',
    'bold',
    'elegant',
    'vibrant',
    'calm',
    'energetic'
]

SEASONAL_THEMES = {
    'spring': ['fresh', 'bright', 'floral', 'pastel'],
    'summer': ['vibrant', 'sunny', 'tropical', 'energetic'],
    'fall': ['warm', 'cozy', 'earthy', 'rustic'],
    'winter': ['cool', 'crisp', 'festive', 'elegant']
}

# Prompt templates
PROMPT_STYLES = [
    'photorealistic',
    'illustration',
    '3d_render',
    'watercolor',
    'digital_art',
    'minimalist',
    'vintage',
    'futuristic'
]

# File naming
TIMESTAMP_FORMAT = '%Y%m%d_%H%M%S'
CREATIVE_PREFIX = 'creative'
CAPTION_PREFIX = 'caption'

# ZIP settings
ZIP_FILENAME = 'creatives.zip'
MAX_ZIP_SIZE_MB = 500
