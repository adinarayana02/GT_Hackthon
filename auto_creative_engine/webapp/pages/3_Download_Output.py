"""
Streamlit page for downloading output.
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from webapp.ui import render_header, render_download_section, render_results_preview

# Page config
st.set_page_config(
    page_title="Download Output - AI Creative Engine",
    page_icon="📥",
    layout="wide"
)

# Render UI
render_header()

st.markdown("### Step 3: Download Your Creatives")

# Check for results
if "results" not in st.session_state:
    st.warning("⚠️ No results available. Please generate creatives first.")
    if st.button("← Back to Generation"):
        st.switch_page("webapp/pages/2_Generate_Creatives.py")
    st.stop()

results = st.session_state.get("results", {})
zip_path = st.session_state.get("zip_path")

# Show results preview
render_results_preview(results)

# Download section
render_download_section(zip_path)

# Show mapping info
if results.get("captions"):
    st.subheader("📋 Caption Mapping")
    with st.expander("View Caption Mappings"):
        for img_name, caption in list(results["captions"].items())[:5]:
            st.write(f"**{img_name}:** {caption[:100]}...")
        if len(results["captions"]) > 5:
            st.info(f"... and {len(results["captions"]) - 5} more")

# Restart button
st.markdown("---")
if st.button("🔄 Start New Generation", type="primary"):
    # Clear session state
    for key in list(st.session_state.keys()):
        if key not in ["api_key"]:  # Keep API key
            del st.session_state[key]
    st.switch_page("webapp/pages/1_Upload_Images.py")

