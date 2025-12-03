"""
Streamlit page for uploading images.
"""

import streamlit as st
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from webapp.ui import render_header, render_file_upload, render_product_description

# Page config
st.set_page_config(
    page_title="Upload Images - AI Creative Engine",
    page_icon="📤",
    layout="wide"
)

# Render UI
render_header()

st.markdown("### Step 1: Upload Your Brand Assets")

# File uploads
logo_file, product_file = render_file_upload()

# Product description
description = render_product_description()

# Store in session state
if logo_file:
    # Save uploaded file
    upload_dir = Path(__file__).parent.parent.parent / "data" / "input"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    logo_path = upload_dir / f"logo_{logo_file.name}"
    with open(logo_path, "wb") as f:
        f.write(logo_file.getbuffer())
    
    st.session_state["logo_path"] = logo_path
    st.success(f"✅ Logo uploaded: {logo_file.name}")

if product_file:
    upload_dir = Path(__file__).parent.parent.parent / "data" / "input"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    product_path = upload_dir / f"product_{product_file.name}"
    with open(product_path, "wb") as f:
        f.write(product_file.getbuffer())
    
    st.session_state["product_path"] = product_path
    st.success(f"✅ Product image uploaded: {product_file.name}")

if description:
    st.session_state["product_description"] = description
    st.success("✅ Product description saved")

# Navigation
if st.button("➡️ Continue to Generation", type="primary"):
    if description:
        st.switch_page("pages/2_Generate_Creatives.py")
    else:
        st.error("Please provide a product description before continuing.")

