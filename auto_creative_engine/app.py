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

# UI imports
from webapp.ui import (
    render_header,
    render_sidebar,
    render_hero_section,
    render_agenda_section,
    render_feature_grid,
    render_quick_steps,
    render_config_status,
)


# Main app
def main():
    """Main application function."""
    
    render_header()

    # Sidebar + session state
    config = render_sidebar()
    for key, value in config.items():
        st.session_state[key] = value

    render_hero_section()
    render_config_status()
    render_agenda_section()
    render_feature_grid()
    render_quick_steps()

    st.markdown("---")
    st.subheader("🚀 Quick Start")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📤 Start Upload", type="primary", use_container_width=True):
            st.switch_page("pages/1_Upload_Images.py")

    with col2:
        if st.button("📖 View Documentation", use_container_width=True):
            st.info("Check the README.md file for detailed documentation.")

if __name__ == "__main__":
    main()

