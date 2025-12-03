"""
Theme service for managing creative themes and variations.
"""

from typing import List, Dict
from datetime import datetime

from ..config.constants import THEMES, SEASONAL_THEMES
from ..utils.logger import get_logger

logger = get_logger()


class ThemeService:
    """Manages themes and seasonal variations."""
    
    def __init__(self):
        logger.info("Initialized ThemeService")
    
    def get_available_themes(self) -> List[str]:
        """Get list of available themes."""
        return THEMES.copy()
    
    def get_seasonal_theme(self, month: Optional[int] = None) -> str:
        """Get seasonal theme based on month."""
        if month is None:
            month = datetime.now().month
        
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'fall'
    
    def get_seasonal_variations(self, season: Optional[str] = None) -> List[str]:
        """Get seasonal theme variations."""
        if season is None:
            season = self.get_seasonal_theme()
        
        return SEASONAL_THEMES.get(season, ['modern', 'vibrant'])
    
    def get_theme_attributes(self, theme: str) -> Dict[str, str]:
        """Get attributes for a specific theme."""
        theme_map = {
            'modern': {
                'style': 'clean',
                'colors': 'neutral',
                'mood': 'sophisticated'
            },
            'minimalist': {
                'style': 'simple',
                'colors': 'monochrome',
                'mood': 'calm'
            },
            'luxury': {
                'style': 'elegant',
                'colors': 'rich',
                'mood': 'premium'
            },
            'playful': {
                'style': 'fun',
                'colors': 'bright',
                'mood': 'energetic'
            },
            'professional': {
                'style': 'corporate',
                'colors': 'conservative',
                'mood': 'trustworthy'
            }
        }
        
        return theme_map.get(theme, theme_map['modern'])

