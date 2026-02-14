# ◆ Deal Sourcing

AI-powered VC deal sourcing tool. Select an industry, stage, and scoring KPIs — the tool uses Claude with web search to find real startups matching your investment criteria.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red)
![Claude API](https://img.shields.io/badge/Claude-Sonnet%204-purple)

## Features

- **Stage-mapped KPIs** — Pre-Seed through Growth, each with relevant scoring criteria
- **Live web research** — Claude searches the web in real-time to find actual companies
- **KPI match scoring** — Each result scored 0-100 against your selected criteria
- **CSV export** — Download results for your pipeline/CRM
- **Custom KPIs** — Add your own scoring criteria on top of defaults

## Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/deal-sourcing.git
cd deal-sourcing

# Install
pip install -r requirements.txt

# Add your API key
echo 'ANTHROPIC_API_KEY = "sk-ant-your-key-here"' > .streamlit/secrets.toml

# Run
streamlit run app.py
```

You'll need an [Anthropic API key](https://console.anthropic.com/).

## Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file path: `app.py`
5. Go to **Settings → Secrets** and add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
6. Deploy

## Project Structure

```
deal-sourcing/
├── .streamlit/
│   └── config.toml      # Theme & server config
├── app.py                # Main Streamlit app
├── config.py             # Industries, stages, KPI mappings
├── research.py           # Claude API + web search logic
├── requirements.txt
└── README.md
```

## Cost

Each search costs ~$0.02-0.05 in Claude API usage depending on result count and search depth.

## License

MIT
