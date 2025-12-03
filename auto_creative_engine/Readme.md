# 🎨 AI Auto-Creative Engine

**Generative AI System for Automatic Ad Creative Production**

**Track:** Generative AI & Marketing Tech  
**Hackathon Problem Statement:** H-003 | The AI Creative Studio

---

## 📋 Overview

Brands often spend weeks manually designing variations of marketing creatives. The **AI Auto-Creative Engine** automates this entire workflow:

1. **Upload** a logo + product image
2. **Automatically generate** 10+ ad creative prompts
3. **Generate** high-quality AI ad images using Gemini Imagen
4. **Produce** matching marketing captions using Gemini 1.5 Flash
5. **Export** a ZIP containing images + captions

This system demonstrates end-to-end automation of marketing content creation using LLMs and image-generation models.

---

## 🧭 Main Agenda (Judge-Friendly)

- ✔ Automate the entire ad creative production workflow — from product image + logo → to final ad creatives → to captions → to downloadable ZIP.
- ✔ Use Generative AI to speed up design cycles — convert work that takes days or weeks into seconds.
- ✔ Enable brands to create 10+ creative variations effortlessly — with different backgrounds, styles, themes, and layouts.
- ✔ Use AI models (LLMs + image models) to generate intelligent prompts, high-quality ads, and brand-consistent captions.
- ✔ Provide a simple tool where anyone can upload assets and instantly get ad-ready creatives.

---

## ✨ Key Features

### Core AI Capabilities

- ✨ **LLM-powered prompt generation** - Gemini 1.5 Flash creates diverse, creative prompts
- 📝 **Gemini-created advertising captions** - Engaging social media captions
- 🖼️ **Gemini Imagen-based ad image generation** - High-quality images
- 🎨 **Theme-based creative variations** - Multiple style options
- 🎨 **Brand color extraction from logo** - Automatic color palette detection
- 📊 **JSON mapping: image → caption** - Structured output

### Full Workflow Automation

- 📤 **Upload → Generate → Review → Download**
- 🖥️ **Streamlit-based user-friendly interface**
- 📦 **Automatic ZIP packaging**

### Production-Ready Engineering

- 🏗️ **Modular backend architecture**
- 🧹 **Clean separation of concerns**
- ⚙️ **Configurable settings** (API keys, models, parameters)

---

## 🛠️ Tech Stack

- **Languages & Frameworks:** Python 3.10+, Streamlit (Frontend UI)
- **AI Models & APIs:**
  - Google Gemini 1.5 Flash (prompt/caption generation)
  - Gemini Imagen 3 (image generation)
- **Libraries:** `google-generativeai`, `dotenv`, `Pillow`, `streamlit`, `scikit-learn`

---

## 📂 Project Structure

```
auto_creative_engine/
│── app.py                 # Main Streamlit app
│── engine.py              # CLI runner
│── README.md              # This file
│── requirements.txt       # Dependencies
│── run.sh                 # Setup & run script
│── setup_env.py           # Environment setup helper
│
├── data/
│   ├── input/             # Uploaded images
│   ├── outputs/
│   │   ├── images/        # Generated creatives
│   │   ├── captions/      # Generated captions
│   │   └── creatives.zip  # Final package
│   ├── metadata/          # Metadata storage
│   └── temp/              # Temporary files
│
├── src/
│   ├── config/            # Configuration
│   ├── llm/               # LLM clients & generators
│   ├── image_gen/         # Image generation (Gemini Imagen)
│   ├── pipeline/          # Main pipeline
│   ├── services/          # Brand services
│   └── utils/             # Utilities
│
├── webapp/
│   ├── ui.py              # UI components
│   ├── pages/             # Streamlit pages
│   └── styles.css         # Custom styles
│
└── tests/                 # Test files
```

---

## 🚀 Installation

### 1. Clone the Repo

```bash
git clone https://github.com/adinarayana02/GT_Hackthon.git
cd auto_creative_engine
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API Key

Create `.env` file:

```bash
python setup_env.py
```

Edit `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_key_here
```

---

## 🎯 How It Works (Architecture)

### High-Level Pipeline

```
+------------------+
| Brand Inputs     |
| Logo + Product   |
+---------+--------+
          |
          v
+-----------------------------+
| LLM Prompt Generator        |
| (Gemini 1.5 Flash)          |
+-----------------------------+
          |
          v
+-----------------------------+
| Image Generation            |
| (Gemini Imagen 3)           |
+-----------------------------+
          |
          v
+-----------------------------+
| Caption Generator           |
| (Gemini 1.5 Flash)          |
+-----------------------------+
          |
          v
+-----------------------------+
| ZIP Packaging + Downloads   |
+-----------------------------+
```

### Workflow Explanation

1. **Upload Inputs:** Brand logo and product image
2. **Generate Prompts:** Gemini 1.5 Flash generates 10+ creative prompts
3. **Generate Images:** Gemini Imagen receives prompts and produces high-quality ad creatives
4. **Generate Captions:** Gemini writes 1 short ad caption per creative
5. **Package:** System produces `creatives.zip` (images, captions, mapping.json)

---

## 🏃 Running the Application

### Streamlit UI (Recommended)

```bash
streamlit run app.py
```

Open browser at `http://localhost:8501`

### CLI Runner

```bash
python engine.py \
  --product-description "A premium wireless headphone with noise cancellation" \
  --num-creatives 10 \
  --brand-name "TechBrand" \
  --api-key your_api_key_here
```

---

## 📦 Output Format

Example ZIP structure:

```
creatives.zip
│
├── images/
│   ├── creative_001.jpg
│   ├── creative_002.jpg
│   ├── ...
│
├── captions/
│   ├── creative_001.txt
│   ├── creative_002.txt
│   ├── ...
│
└── mapping.json
```

`mapping.json` format:

```json
{
  "mapping": {
    "creative_001": "Discover our amazing product! ✨ Shop now!",
    "creative_002": "Elevate your experience today! 🚀",
    ...
  },
  "count": 10
}
```

---

## 🎨 Features in Detail

### 1. Prompt Generation

- Uses Gemini 1.5 Flash to create diverse, creative prompts
- Incorporates brand colors, themes, and product details
- Generates 10+ unique variations

### 2. Image Generation

- Gemini Imagen 3 for high-quality images
- Supports multiple aspect ratios
- Automatic retry on failures

### 3. Caption Generation

- Gemini 1.5 Flash creates engaging social media captions
- Matches brand tone and style
- Includes call-to-action

### 4. Brand Color Extraction

- Automatically extracts dominant colors from logo
- Uses K-means clustering
- Applies colors to creative generation

---

## ⚙️ Configuration

### Environment Variables

- `GEMINI_API_KEY` - Required for Gemini API access
- `DEFAULT_LLM_PROVIDER` - LLM provider (default: gemini)
- `DEFAULT_IMAGE_MODEL` - Image model (default: imagen3)
- `DEFAULT_NUM_CREATIVES` - Default number of creatives (default: 10)
- `LOG_LEVEL` - Logging level (default: INFO)

### Settings

Modify `src/config/settings.py` to adjust:

- Image aspect ratios
- LLM models and parameters
- Theme options
- Output directories

---

## 🧪 Testing

Run tests:

```bash
python -m pytest tests/
```

---

## 📊 Limitations & Future Work

### Current Limitations

- Requires Gemini API key
- Image generation rate limits apply
- Image generation can take time per image

### Future Enhancements

- [ ] Batch processing for multiple products
- [ ] A/B testing framework
- [ ] Analytics dashboard
- [ ] Custom template support
- [ ] Multi-language captions

---

## 🤝 Contributing

This is a hackathon project. Contributions welcome!

---

## 📄 License

This project is created for the GT Hackathon. All rights reserved.

---

## 👤 Author

**Adi Narayana Thota**

- GitHub: [@adinarayana02](https://github.com/adinarayana02)

---

## 🙏 Acknowledgments

- Google for Gemini API
- Streamlit for the amazing UI framework
- All open-source contributors

---

**Built with ❤️ for the GT Hackathon**
