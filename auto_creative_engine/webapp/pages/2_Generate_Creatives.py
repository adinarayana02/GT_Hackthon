"""
Streamlit page for generating creatives.
"""

import streamlit as st
from pathlib import Path
import sys
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from webapp.ui import render_header, render_generation_status
from src.pipeline.orchestrator import Orchestrator
from src.config.settings import GenerationSettings, BrandConfig
from src.pipeline.packager import Packager

# Page config
st.set_page_config(
    page_title="Generate Creatives - AI Creative Engine",
    page_icon="🎨",
    layout="wide"
)

# Render UI
render_header()

st.markdown("### Step 2: Generate Ad Creatives")

# Check session state
if "product_description" not in st.session_state:
    st.warning("⚠️ Please go back and provide a product description.")
    if st.button("← Back to Upload"):
        st.switch_page("webapp/pages/1_Upload_Images.py")
    st.stop()

# Get configuration from sidebar (if available) or use defaults
api_key = st.session_state.get("api_key", "")
num_creatives = st.session_state.get("num_creatives", 10)
brand_name = st.session_state.get("brand_name", "Brand")
theme = st.session_state.get("theme", "modern")

# Display current settings
col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"**Brand:** {brand_name}")
with col2:
    st.info(f"**Creatives:** {num_creatives}")
with col3:
    st.info(f"**Theme:** {theme}")

# API Key input
if not api_key:
    api_key = st.text_input("Gemini API Key", type="password", help="Required for generation")
    if api_key:
        st.session_state["api_key"] = api_key

# Generate button
if st.button("🚀 Generate Creatives", type="primary", disabled=not api_key):
    if not api_key:
        st.error("Please provide a Gemini API key.")
        st.stop()
    
    # Initialize settings
    settings = GenerationSettings()
    settings.num_creatives = num_creatives
    settings.brand_config = BrandConfig(
        name=brand_name,
        theme=theme,
        tone="professional"
    )
    
    # Get file paths from session state
    logo_path = st.session_state.get("logo_path")
    product_path = st.session_state.get("product_path")
    product_description = st.session_state.get("product_description")
    
    # Initialize orchestrator
    try:
        orchestrator = Orchestrator(settings=settings, api_key=api_key)
        
        # Show progress
        render_generation_status("generating")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Generate
        status_text.text("Initializing...")
        progress_bar.progress(10)
        
        status_text.text("Generating prompts...")
        progress_bar.progress(30)
        time.sleep(0.5)
        
        status_text.text("Generating images with Gemini Imagen...")
        progress_bar.progress(50)
        
        results = orchestrator.run(
            product_description=product_description,
            logo_path=logo_path,
            product_image_path=product_path,
            num_creatives=num_creatives,
            brand_name=brand_name
        )
        
        progress_bar.progress(80)
        status_text.text("Generating captions...")
        time.sleep(0.5)
        
        # Package results
        packager = Packager()
        zip_path = packager.create_zip_from_results(
            results=results,
            output_dir=settings.output_dir,
            brand_name=brand_name
        )
        
        progress_bar.progress(100)
        status_text.text("Complete!")
        
        # Store results
        st.session_state["results"] = results
        st.session_state["zip_path"] = zip_path
        
        render_generation_status("complete")
        st.success(f"✅ Successfully generated {results['count']} creatives!")
        
        # Show preview
        if results.get("images"):
            st.subheader("Preview")
            preview_images = results["images"][:3]
            cols = st.columns(3)
            for idx, img_path in enumerate(preview_images):
                with cols[idx]:
                    try:
                        from PIL import Image
                        img = Image.open(img_path)
                        st.image(img, caption=f"Creative {idx+1}", use_container_width=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        # Navigate to download
        if st.button("📥 Go to Download", type="primary"):
            st.switch_page("webapp/pages/3_Download_Output.py")
    
    except Exception as e:
        render_generation_status("error")
        st.error(f"Error during generation: {str(e)}")
        st.exception(e)

# Back button
if st.button("← Back"):
    st.switch_page("webapp/pages/1_Upload_Images.py")

