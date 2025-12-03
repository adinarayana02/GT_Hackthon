"""
Google Gemini Imagen client for image generation.
"""

import base64
import requests
from typing import Optional, List
from pathlib import Path
from io import BytesIO

from PIL import Image

from ..config.settings import ImageGenConfig
from ..utils.logger import get_logger
from ..utils.file_utils import ensure_dir

logger = get_logger()


class GeminiImageClient:
    """Client for Gemini Imagen image generation."""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[ImageGenConfig] = None):
        self.config = config or ImageGenConfig(model='imagen3')
        self.api_key = api_key or self.config.api_key
        
        if not self.api_key:
            raise ValueError("Gemini API key is required for image generation")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:generateImages"
        logger.info("Initialized Gemini Imagen client")
    
    def generate_image(
        self,
        prompt: str,
        number_of_images: int = 1,
        aspect_ratio: str = "1:1",
        output_path: Optional[Path] = None
    ) -> Path:
        """Generate a single image using Gemini Imagen."""
        try:
            logger.info(f"Generating image with Gemini Imagen: {prompt[:50]}...")
            
            url = f"{self.base_url}?key={self.api_key}"
            
            payload = {
                "prompt": prompt,
                "number_of_images": number_of_images,
                "aspect_ratio": aspect_ratio
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract base64 image data
            if "generatedImages" in result and len(result["generatedImages"]) > 0:
                image_data = result["generatedImages"][0]["imageBytes"]
                image_bytes = base64.b64decode(image_data)
            else:
                raise ValueError("No image generated in response")
            
            # Save the image
            if output_path is None:
                output_path = Path(__file__).parent.parent.parent / 'data' / 'temp' / 'gemini_output.jpg'
            
            ensure_dir(output_path.parent)
            
            with Image.open(BytesIO(image_bytes)) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output_path, 'JPEG', quality=95)
            
            logger.info(f"Generated image saved to {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error generating image with Gemini Imagen: {e}")
            # Fallback: Try using Vertex AI Imagen API format
            try:
                return self._generate_with_vertex_api(prompt, output_path)
            except Exception as e2:
                logger.error(f"Fallback also failed: {e2}")
                raise
    
    def _generate_with_vertex_api(self, prompt: str, output_path: Optional[Path] = None) -> Path:
        """Alternative method using Vertex AI format."""
        # This is a placeholder - Vertex AI requires project setup
        # For now, we'll use a simpler approach
        raise NotImplementedError("Vertex AI setup required for this method")
    
    def generate_images(
        self,
        prompts: List[str],
        output_dir: Path,
        aspect_ratio: str = "1:1"
    ) -> List[Path]:
        """Generate multiple images from prompts."""
        output_paths = []
        
        for i, prompt in enumerate(prompts):
            try:
                output_path = output_dir / f"creative_{i+1:03d}.jpg"
                path = self.generate_image(
                    prompt,
                    aspect_ratio=aspect_ratio,
                    output_path=output_path
                )
                output_paths.append(path)
                logger.info(f"Generated image {i+1}/{len(prompts)}")
            
            except Exception as e:
                logger.error(f"Failed to generate image {i+1}: {e}")
                continue
        
        logger.info(f"Generated {len(output_paths)}/{len(prompts)} images")
        return output_paths

