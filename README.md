# TrailGear AI Agent

**A conversational product assistant powered by the Claude API.**

👉 **[View Live App](https://trailgear-ai-agent-danibaum.streamlit.app/)**

---

## Overview

TrailGear AI Agent is a natural language product assistant for a fictional outdoor gear retailer. Instead of browsing filters and search bars, customers can ask plain English questions and get instant, accurate answers drawn directly from the product catalog.

Built to demonstrate how LLMs can replace traditional product search interfaces in retail and e-commerce contexts.

## Demo

Ask questions like:
- *What waterproof jackets do you have under 200 EUR?*
- *I need a sleeping bag rated for -10°C trips.*
- *What is the lightest tent in the range?*
- *Which products have EN certifications?*
- *Recommend a full kit for a 3-day hiking trip.*

## How It Works

1. A 60-product catalog is loaded from a structured CSV file at startup.
2. The full catalog is injected into the Claude API system prompt as context.
3. The user's question along with the full conversation history is sent to Claude with each request.
4. Claude returns a grounded, catalog-accurate answer with product names and prices.

No vector database or semantic search required at this scale. The entire catalog fits cleanly within the model's context window.

## Tech Stack

| Layer | Tool |
|---|---|
| LLM | Claude API (claude-opus-4-6) by Anthropic |
| Frontend | Streamlit |
| Data | Pandas + CSV |
| Environment | python-dotenv |
| Deployment | Streamlit Community Cloud |

## Project Structure

```
├── app.py              # Main Streamlit application
├── catalog.csv         # 60-product outdoor gear catalog
├── requirements.txt    # Python dependencies
├── .env.example        # API key template
└── .streamlit/
    └── config.toml     # Streamlit configuration
```

## Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/danibaum8/trailgear-ai-agent.git
cd trailgear-ai-agent

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
cp .env.example .env
# Edit .env and replace with your Anthropic API key

# 5. Run the app
streamlit run app.py
```

## Author

**Dani Baumgarten** | Data Analyst & AI Solutions Builder based in Ireland

[LinkedIn](https://www.linkedin.com/in/danibaum8/) · [Kaggle](https://www.kaggle.com/danibaum) · [Tableau](https://public.tableau.com/app/profile/dani.baum/vizzes)
