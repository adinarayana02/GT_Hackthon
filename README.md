# AI Auto-Creative Engine

### Generative AI System for Automatic Ad Creative Production
**Track:** Generative AI & Marketing Tech  
**Hackathon Problem Statement:** H-003 | The AI Creative Studio

---

##  Overview
Brands often spend weeks manually designing variations of marketing creatives.  
The AI Auto-Creative Engine automates this entire workflow:
- Upload a logo + product image
- Automatically generate 10+ ad creative prompts
- Generate high-quality AI ad images using DALL·E 3 / SDXL
- Produce matching marketing captions using GPT
- Export a ZIP containing images + captions

This system demonstrates end-to-end automation of marketing content creation using LLMs and image-generation models.

---

## Key Features
### Core AI Capabilities
- LLM-powered prompt generation
- GPT-created advertising captions
- DALL·E 3-based ad image generation
- Theme-based creative variations
- Brand color extraction from logo
- JSON mapping: image → caption

### Full Workflow Automation
- Upload → Generate → Review → Download
- Streamlit-based user-friendly interface
- Automatic ZIP packaging

### Production-Ready Engineering
- Modular backend architecture
- Clean separation of concerns
- Configurable settings (API keys, models, parameters)
- Supports scaling to multiple models (SDXL, ControlNet)

---

## Tech Stack
- **Languages & Frameworks:** Python 3.10+, Streamlit (Frontend UI)
- **AI Models & APIs:** OpenAI GPT-4o/GPT-4.1 (prompt/caption generation), DALL·E 3 (image generation), SDXL & ControlNet (optional)
- **Libraries:** openai, dotenv, Pillow, streamlit

---

## Project Structure

```bash
auto_creative_engine/
│── app.py
│── engine.py
│── README.md
│── requirements.txt
│── run.sh
│── .env.example
│
├── data/
│   ├── input/
│   ├── outputs/
│   │   ├── images/
│   │   ├── captions/
│   │   └── creatives.zip
│   ├── metadata/
│   └── temp/
│
├── src/
│   ├── config/
│   ├── llm/
│   ├── image_gen/
│   ├── pipeline/
│   ├── services/
│   └── utils/
│
├── webapp/
│   ├── ui.py
│   ├── pages/
│   ├── assets/
│   └── styles.css
│
└── tests/
```

---

## Installation

1. **Clone the Repo**
    ```bash
    git clone https://github.com/adinarayana02/GT_Hackthon.git
    cd auto_creative_engine
    ```
2. **Create Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate       # Mac/Linux
    venv\Scripts\activate          # Windows
    ```
3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Add API Key**
    Create .env file:
    ```ini
    OPENAI_API_KEY=your_key_here
    ```

---

## How It Works (Architecture)

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
| (GPT-4o)                    |
+-----------------------------+
          |
          v
+-----------------------------+
| Image Generation            |
| (DALL·E 3 / SDXL)           |
+-----------------------------+
          |
          v
+-----------------------------+
| Caption Generator (GPT-4o) |
+-----------------------------+
          |
          v
+-----------------------------+
| ZIP Packaging + Downloads   |
+-----------------------------+
```

---

## Workflow Explanation
1. **Upload Inputs:** Brand logo and product image.
2. **Generate Prompts:** GPT-4o generates 10+ creative prompts (lighting, composition, background, brand colors, seasonal themes).
3. **Generate Images:** DALL·E receives prompts and product details to produces high-quality ad creatives.
4. **Generate Captions:** GPT writes 1 short ad caption per creative (stored in /data/outputs/captions/).
5. **Package:** System produces creatives.zip (images, captions, mapping.json).

---

## Running the Application

**Streamlit UI**
```bash
streamlit run app.py
```
Open browser at `http://localhost:8501`

**CLI Runner**
```bash
python engine.py
```

---

## Output Format
Example ZIP structure:
```
creatives.zip
│
├── images/
│   ├── ad_01.png
│   ├── ad_02.png
│   ├── ...
│
├── captions/
│   ├── ad_01.txt
│   ├── ad_02.txt
│   ├── ...
│
└── mapping.json
```

---

##  Testing
Unit tests using pytest:
```
pytest tests/
```
**Coverage:** Prompt generation, caption generation, image pipeline, ZIP packager.

---

## Future Enhancements
- Multi-language caption generation
- Brand style learning from previous creatives
- A/B testing caption generator
- Custom SDXL fine-tuning
- Template-based design mixing
- Auto-layout with product positioning

---

##  Why This Solution Stands Out
- 100% automated creative pipeline
- High-quality imagery
- Brand-consistent content
- Professional engineering
- Very polished UI
- Ready for real marketing teams
- Designed for production deployment

---

> Made for GroundTruth AI Hackathon 2025
