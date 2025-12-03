"""
LLM client for Google Gemini API.
"""

from typing import Optional
import google.generativeai as genai

from ..config.settings import LLMConfig
from ..utils.logger import get_logger

logger = get_logger()


class GeminiClient:
    """Google Gemini client for text generation."""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig(provider='gemini')
        self.api_key = api_key or self.config.api_key
        
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        genai.configure(api_key=self.api_key)
        model_name = self.config.model or 'gemini-1.5-flash'
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        logger.info(f"Initialized Gemini client with model: {model_name}")
    
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate text using Google Gemini."""
        try:
            temperature = temperature if temperature is not None else self.config.temperature
            
            # Update model if specified
            if model and model != self.model_name:
                self.model_name = model
                self.model = genai.GenerativeModel(model)
                logger.debug(f"Switched to model: {model}")
            
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens or self.config.max_tokens,
            }
            
            # Add system instruction
            full_prompt = f"You are a creative AI assistant specialized in generating marketing content and ad creatives.\n\n{prompt}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config,
                **kwargs
            )
            
            content = response.text
            logger.debug(f"Generated text with Gemini")
            return content.strip()
        
        except Exception as e:
            logger.error(f"Error generating text with Gemini: {e}")
            raise


def get_llm_client(api_key: Optional[str] = None, config: Optional[LLMConfig] = None):
    """Get Gemini LLM client."""
    return GeminiClient(api_key=api_key, config=config)
