"""
CLI engine for running the creative generation pipeline.
"""

import argparse
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline.orchestrator import Orchestrator
from src.config.settings import GenerationSettings, BrandConfig
from src.pipeline.packager import Packager
from src.utils.logger import get_logger

logger = get_logger()

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI Auto-Creative Engine - Generate ad creatives from product descriptions"
    )
    
    parser.add_argument(
        "--product-description",
        type=str,
        required=True,
        help="Description of the product to create ads for"
    )
    
    parser.add_argument(
        "--logo",
        type=Path,
        help="Path to brand logo image (optional)"
    )
    
    parser.add_argument(
        "--product-image",
        type=Path,
        help="Path to product image (optional)"
    )
    
    parser.add_argument(
        "--num-creatives",
        type=int,
        default=10,
        help="Number of creatives to generate (default: 10)"
    )
    
    parser.add_argument(
        "--brand-name",
        type=str,
        default="Brand",
        help="Brand name (default: Brand)"
    )
    
    parser.add_argument(
        "--theme",
        type=str,
        default="modern",
        choices=["modern", "minimalist", "luxury", "playful", "professional", "bold", "elegant", "vibrant"],
        help="Creative theme (default: modern)"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        help="Gemini API key (or set GEMINI_API_KEY env var)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory (default: data/outputs)"
    )
    
    args = parser.parse_args()
    
    # Initialize settings
    settings = GenerationSettings()
    settings.num_creatives = args.num_creatives
    settings.brand_config = BrandConfig(
        name=args.brand_name,
        theme=args.theme,
        tone="professional"
    )
    
    if args.output_dir:
        settings.output_dir = args.output_dir
    
    # Get API key
    api_key = args.api_key
    if not api_key:
        from src.config.env import GEMINI_API_KEY
        api_key = GEMINI_API_KEY
    
    if not api_key:
        logger.error("Gemini API key is required. Provide --api-key or set GEMINI_API_KEY env var.")
        sys.exit(1)
    
    # Validate inputs
    if args.logo and not args.logo.exists():
        logger.error(f"Logo file not found: {args.logo}")
        sys.exit(1)
    
    if args.product_image and not args.product_image.exists():
        logger.error(f"Product image not found: {args.product_image}")
        sys.exit(1)
    
    # Run generation
    try:
        logger.info("Starting creative generation...")
        
        orchestrator = Orchestrator(settings=settings, api_key=api_key)
        
        results = orchestrator.run(
            product_description=args.product_description,
            logo_path=args.logo,
            product_image_path=args.product_image,
            num_creatives=args.num_creatives,
            brand_name=args.brand_name
        )
        
        # Package results
        packager = Packager()
        zip_path = packager.create_zip_from_results(
            results=results,
            output_dir=settings.output_dir,
            brand_name=args.brand_name
        )
        
        logger.info(f"✅ Generation complete!")
        logger.info(f"   - Generated {results['count']} images")
        logger.info(f"   - Created {len(results['captions'])} captions")
        logger.info(f"   - ZIP package: {zip_path}")
        
        print(f"\n✅ Success! Generated {results['count']} creatives.")
        print(f"📦 ZIP package: {zip_path}")
    
    except Exception as e:
        logger.error(f"Error during generation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

