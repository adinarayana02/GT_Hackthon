from typing import Optional, List
from pathlib import Path
from io import BytesIO

from PIL import Image
from google.genai import Client, types

from ..config.settings import ImageGenConfig
from ..utils.logger import get_logger
from ..utils.file_utils import ensure_dir

logger = get_logger()


class GeminiImageClient:
    """Client for Gemini Imagen image generation."""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[ImageGenConfig] = None):
        self.config = config or ImageGenConfig(model='imagen4')
        self.api_key = api_key or self.config.api_key
        
        if not self.api_key:
            raise ValueError("Gemini API key is required for image generation")
        
        self.client = Client(api_key=self.api_key)
        logger.info("Initialized Google Gen AI client for Imagen")
    
    def generate_image(
        self,
        prompt: str,
        number_of_images: int = 1,
        aspect_ratio: str = "1:1",
        output_path: Optional[Path] = None
    ) -> Path:
        """Generate a single image using Gemini Imagen."""
        try:
            logger.info(f"Generating image with Imagen: {prompt[:50]}...")
            
            gen_cfg = types.GenerateImagesConfig(
                number_of_images=number_of_images,
                aspect_ratio=aspect_ratio,
            )
            
            result = self.client.models.generate_images(
                model='imagen-4.0-generate-001',
                prompt=prompt,
                config=gen_cfg,
            )
            
            images = getattr(result, "generated_images", [])
            if not images:
                raise ValueError("No image generated in response")
            first = images[0]
            img_obj = getattr(first, "image", None)
            
            if output_path is None:
                output_path = Path(__file__).parent.parent.parent / 'data' / 'temp' / 'gemini_output.jpg'
            
            ensure_dir(output_path.parent)
            
            if img_obj is not None:
                if getattr(img_obj, "mode", None) != 'RGB':
                    img_obj = img_obj.convert('RGB')
                img_obj.save(output_path, 'JPEG', quality=95)
            else:
                data = getattr(first, "data", None)
                if data is None:
                    raise ValueError("No image data in response")
                with Image.open(BytesIO(data)) as img:
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
        ensure_dir(output_dir)
        
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        def _task(idx_prompt):
            i, prompt = idx_prompt
            out = output_dir / f"creative_{i+1:03d}.jpg"
            return self.generate_image(prompt, aspect_ratio=aspect_ratio, output_path=out)
        
        with ThreadPoolExecutor(max_workers=min(6, len(prompts))) as ex:
            futures = {ex.submit(_task, (i, p)): i for i, p in enumerate(prompts)}
            for fut in as_completed(futures):
                i = futures[fut]
                try:
                    path = fut.result()
                    output_paths.append(path)
                    logger.info(f"Generated image {i+1}/{len(prompts)}")
                except Exception as e:
                    logger.error(f"Failed to generate image {i+1}: {e}")
        
        logger.info(f"Generated {len(output_paths)}/{len(prompts)} images")
        return output_paths

