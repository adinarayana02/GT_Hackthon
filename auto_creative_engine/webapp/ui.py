"""
Streamlit UI components and helpers.
"""

import streamlit as st
from pathlib import Path
from typing import Optional

def render_header():
    """Render the application header."""
    st.title("🎨 AI Auto-Creative Engine")
    st.markdown("### Generative AI System for Automatic Ad Creative Production")
    st.markdown("---")

def render_sidebar():
    """Render sidebar configuration."""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Enter your Google Gemini API key"
        )
        
        # Number of creatives
        num_creatives = st.slider(
            "Number of Creatives",
            min_value=1,
            max_value=20,
            value=10,
            help="How many ad creatives to generate"
        )
        
        # Brand name
        brand_name = st.text_input(
            "Brand Name",
            value="Brand",
            help="Your brand name"
        )
        
        # Theme selection
        theme = st.selectbox(
            "Theme",
            options=["modern", "minimalist", "luxury", "playful", "professional", "bold", "elegant", "vibrant"],
            index=0,
            help="Creative theme style"
        )
        
        return {
            "api_key": api_key,
            "num_creatives": num_creatives,
            "brand_name": brand_name,
            "theme": theme
        }

def render_file_upload():
    """Render file upload section."""
    st.subheader("📤 Upload Images")
    
    col1, col2 = st.columns(2)
    
    with col1:
        logo_file = st.file_uploader(
            "Brand Logo",
            type=['png', 'jpg', 'jpeg'],
            help="Upload your brand logo (optional)"
        )
    
    with col2:
        product_file = st.file_uploader(
            "Product Image",
            type=['png', 'jpg', 'jpeg'],
            help="Upload your product image (optional)"
        )
    
    return logo_file, product_file

def render_product_description():
    """Render product description input."""
    st.subheader("📝 Product Description")
    description = st.text_area(
        "Describe your product",
        height=100,
        placeholder="Enter a detailed description of your product...",
        help="This will be used to generate creative prompts"
    )
    return description

def render_generation_status(status: str, progress: Optional[float] = None):
    """Render generation status."""
    if status == "generating":
        st.info("🔄 Generating creatives... This may take a few minutes.")
        if progress:
            st.progress(progress)
    elif status == "complete":
        st.success("✅ Generation complete!")
    elif status == "error":
        st.error("❌ An error occurred during generation.")

def render_results_preview(results: dict):
    """Render preview of generated results."""
    st.subheader("📊 Generation Results")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Images Generated", results.get("count", 0))
    with col2:
        st.metric("Captions Created", len(results.get("captions", {})))
    with col3:
        st.metric("Status", "✅ Complete" if results.get("count", 0) > 0 else "⚠️ Incomplete")
    
    # Show sample images
    if results.get("images"):
        st.subheader("🖼️ Preview")
        images = results["images"][:6]  # Show first 6
        
        cols = st.columns(3)
        for idx, img_path in enumerate(images):
            with cols[idx % 3]:
                try:
                    from PIL import Image
                    img = Image.open(img_path)
                    st.image(img, caption=f"Creative {idx+1}", use_container_width=True)
                except Exception as e:
                    st.error(f"Error loading image: {e}")

def render_download_section(zip_path: Optional[Path] = None):
    """Render download section."""
    st.subheader("📥 Download Output")
    
    if zip_path and zip_path.exists():
        with open(zip_path, 'rb') as f:
            st.download_button(
                label="📦 Download ZIP",
                data=f.read(),
                file_name=zip_path.name,
                mime="application/zip"
            )
        st.info(f"Package contains images, captions, and mapping.json")
    else:
        st.warning("No ZIP file available yet. Generate creatives first.")

