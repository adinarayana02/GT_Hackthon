"""
Helper script to set up .env file.
"""

from pathlib import Path

def setup_env():
    """Create .env file from template."""
    env_example = Path(__file__).parent / ".env.example"
    env_file = Path(__file__).parent / ".env"
    
    if env_file.exists():
        print("⚠️  .env file already exists. Skipping creation.")
        return
    
    if env_example.exists():
        # Read example
        with open(env_example, 'r') as f:
            content = f.read()
        
        # Write .env
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Created .env file from .env.example")
        print("📝 Please update .env with your actual API keys")
    else:
        # Create basic .env
        content = """# Gemini API Key (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# Default settings
DEFAULT_LLM_PROVIDER=gemini
DEFAULT_IMAGE_MODEL=imagen3
DEFAULT_NUM_CREATIVES=10
LOG_LEVEL=INFO
"""
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Created .env file")
        print("📝 Please update .env with your Gemini API key")

if __name__ == "__main__":
    setup_env()
