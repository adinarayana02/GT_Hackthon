# 🚀 Quick Start Guide

## Prerequisites

- Python 3.10 or higher
- Google Gemini API key

## Installation (3 Steps)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

Create a `.env` file in the project root:

```bash
python setup_env.py
```

Edit `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

### 3. Run the Application

**Option A: Streamlit UI (Recommended)**

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

**Option B: CLI**

```bash
python engine.py \
  --product-description "A premium wireless headphone with noise cancellation" \
  --num-creatives 10 \
  --brand-name "TechBrand" \
  --api-key your_api_key_here
```

## Usage Workflow

1. **Upload Images** (Optional)
   - Brand logo
   - Product image

2. **Describe Product**
   - Enter a detailed product description

3. **Generate Creatives**
   - Click "Generate Creatives"
   - Wait for generation (varies by API)

4. **Download Results**
   - Preview generated images
   - Download ZIP package

## Output Structure

```
creatives.zip
├── images/
│   ├── creative_001.jpg
│   ├── creative_002.jpg
│   └── ...
├── captions/
│   ├── creative_001.txt
│   ├── creative_002.txt
│   └── ...
└── mapping.json
```

## Troubleshooting

### API Key Issues
- Make sure your `.env` file is in the project root
- Verify your API key is valid
- Check you have sufficient Gemini API quota

### Generation Errors
- Check internet connection
- Verify API key has access to Gemini Imagen
- Check logs in `data/temp/` directory

### Import Errors
- Make sure you're in the project root directory
- Verify all dependencies are installed: `pip install -r requirements.txt`

## Need Help?

Check the full [README.md](README.md) for detailed documentation.
