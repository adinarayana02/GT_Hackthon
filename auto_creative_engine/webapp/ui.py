"""
Streamlit UI components and helpers.
"""

import streamlit as st
from pathlib import Path
from typing import Optional, List, Dict
from src.config.env import GEMINI_API_KEY


def render_config_status():
    st.subheader("Configuration")
    key_ok = bool(st.session_state.get("api_key") or GEMINI_API_KEY)
    api_status = "Configured" if key_ok else "Missing"
    try:
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        device = "unknown"
    cols = st.columns(3)
    with cols[0]:
        st.info(f"API Key: {api_status}")
    with cols[1]:
        st.info(f"SDXL Device: {device}")
    with cols[2]:
        st.info(f"Creatives per run: {st.session_state.get('num_creatives', 10)}")


def render_header():
    """Render the application header."""
    st.title("🎨 AI Auto-Creative Engine")
    st.markdown("### Generative AI System for Automatic Ad Creative Production")
    st.markdown("---")


def render_hero_section():
    """Render hero section with quick metrics."""
    st.subheader("Design Studio Superpowers, Delivered in Seconds ⚡")
    hero_cols = st.columns([2, 1])
    with hero_cols[0]:
        st.markdown(
            """
            Build agency-grade ad creatives by combining your **logo + product photo** with
            Gemini-powered prompt and image generation. Convert a process that normally takes
            days or weeks into a single click workflow.
            """
        )
        st.markdown(
            """
            - ✅ Upload → Generate → Download, all in one place  
            - ✅ Automatically enforce brand colors, tone, and themes  
            - ✅ Export ready-to-pitch ZIP files with assets + captions  
            """
        )
    with hero_cols[1]:
        st.metric("Creative Variations / Run", "10+")
        st.metric("Time to Delivery", "≈ 90 sec")
        st.metric("Brand Inputs", "Logo + Product")


def render_agenda_section():
    """Show judge-friendly agenda."""
    st.subheader("🎯 Main Agenda (Judge-Friendly)")
    st.markdown(
        """
        - ✔ **Automate the entire ad creative workflow** – from raw assets to downloadable ZIP.  
        - ✔ **Use Generative AI to accelerate design cycles** – hours of manual work in seconds.  
        - ✔ **Enable 10+ creative variations per run** – different backgrounds, styles, and layouts.  
        - ✔ **Leverage LLMs + Image Models** for intelligent prompts, high-quality ads, and
          brand-consistent captions.  
        - ✔ **Provide a simple tool** where anyone can upload assets and get instant creatives.  
        """
    )


def render_feature_grid():
    """Display feature cards."""
    st.subheader("✨ Why teams use the Auto-Creative Engine")
    features = [
        ("⚡ Speed", "Generates campaigns in seconds, not weeks."),
        ("🧠 Smart Prompts", "Gemini 1.5 Flash crafts brand-aware image prompts."),
        ("🖼️ Imagen 3 Output", "High-resolution, on-brand ad creatives every time."),
        ("🎨 Themes", "Modern, luxury, playful, bold, and more with one toggle."),
        ("📋 Captions", "Ready-to-post CTA-driven messaging per creative."),
        ("📦 ZIP Export", "Images, captions, and JSON mapping in one click."),
    ]
    cols = st.columns(3)
    for idx, (title, body) in enumerate(features):
        with cols[idx % 3]:
            st.info(f"**{title}**\n\n{body}")


def render_quick_steps():
    """Highlight the input/process/output pipeline."""
    st.subheader("🧩 Workflow: Input → Process → Output")
    steps = st.columns(3)
    steps[0].markdown(
        """
        **1. Input**  
        - Brand logo  
        - Product photo  
        - Product story / CTA  
        """
    )
    steps[1].markdown(
        """
        **2. Process**  
        - Gemini generates prompts + captions  
        - SDXL renders ad creatives  
        - Brand colors + themes applied  
        """
    )
    steps[2].markdown(
        """
        **3. Output**  
        - 10+ creative variations  
        - Matching captions  
        - Downloadable `creatives.zip`  
        """
    )


def render_sidebar():
    """Render sidebar configuration."""
    with st.sidebar:
        st.header("⚙️ Configuration")

        api_key = st.text_input(
            "Gemini API Key",
            value=GEMINI_API_KEY or "",
            type="password",
            help="Enter your Google Gemini API key"
        )

        num_creatives = st.slider(
            "Number of Creatives",
            min_value=1,
            max_value=20,
            value=10,
            help="How many ad creatives to generate"
        )

        brand_name = st.text_input(
            "Brand Name",
            value="Brand",
            help="Your brand name"
        )

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
    st.caption("Accepted formats: PNG, JPG, JPEG · Recommended size ≥ 1024px for best results.")

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
        height=120,
        placeholder="Enter audience, hero benefit, CTA, mood, platform...",
        help="This will be used to generate creative prompts"
    )
    st.caption("Tip: Include audience, benefits, CTA, mood, and campaign goal.")
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

    if results.get("images"):
        st.subheader("🖼️ Preview")
        images = results["images"][:6]
        cols = st.columns(3)
        for idx, img_path in enumerate(images):
            with cols[idx % 3]:
                try:
                    from PIL import Image
                    img = Image.open(img_path)
                    st.image(img, caption=f"Creative {idx+1}", use_container_width=True)
                except Exception as e:
                    st.error(f"Error loading image: {e}")
    else:
        st.caption("Creatives will appear here after a generation run.")


def render_prompt_caption_panel(
    prompts: Optional[List[str]] = None,
    captions: Optional[Dict[str, str]] = None,
) -> None:
    """Show generated prompts and captions."""
    prompts = prompts or []
    captions = captions or {}

    st.subheader("🧠 Prompts & ✍️ Captions")
    prompt_cols = st.columns(2)
    with prompt_cols[0]:
        st.markdown("**Prompt Samples**")
        if prompts:
            for idx, prompt in enumerate(prompts[:3], start=1):
                st.markdown(f"Prompt {idx}")
                st.write(prompt)
        else:
            st.caption("Prompts will appear after generation.")
    with prompt_cols[1]:
        st.markdown("**Caption Samples**")
        if captions:
            for idx, (img_name, caption) in enumerate(list(captions.items())[:3], start=1):
                st.markdown(f"Caption {idx} · {img_name}")
                st.write(caption)
        else:
            st.caption("Captions will appear after generation.")


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
        st.info("Package contains images, captions, and mapping.json")
    else:
        st.warning("No ZIP file available yet. Generate creatives first.")

