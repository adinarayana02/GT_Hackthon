"""
Main Streamlit application entry point.
"""

import streamlit as st
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Page configuration
st.set_page_config(
    page_title="AI Auto-Creative Engine",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
css_path = Path(__file__).parent / "webapp" / "styles.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main app
def main():
    """Main application function."""
    from webapp.ui import render_header, render_sidebar
    
    # Render header
    render_header()
    
    # Render sidebar
    config = render_sidebar()
    
    # Store config in session state
    for key, value in config.items():
        st.session_state[key] = value
    
    # Main content
    st.markdown("""
    ### Welcome to the AI Auto-Creative Engine! 🚀
    
    This system automates the creation of marketing ad creatives using AI.
    
    **How it works:**
    1. 📤 **Upload** your brand logo and product image
    2. 🎨 **Generate** 10+ unique ad creatives using Gemini Imagen
    3. 📥 **Download** your complete package (images + captions)
    
    **Features:**
    - ✨ LLM-powered prompt generation (Gemini)
    - 🖼️ High-quality Gemini Imagen image generation
    - 📝 Gemini-created advertising captions
    - 🎨 Brand color extraction
    - 📦 Automatic ZIP packaging
    
    **Get Started:**
    Use the sidebar to configure your settings, then navigate through the pages above.
    """)
    
    # Quick start section
    st.markdown("---")
    st.subheader("🚀 Quick Start")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Start Upload", type="primary", use_container_width=True):
            st.switch_page("webapp/pages/1_Upload_Images.py")
    
    with col2:
        if st.button("📖 View Documentation", use_container_width=True):
            st.info("Check the README.md file for detailed documentation.")

if __name__ == "__main__":
    main()

