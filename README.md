# LLM_QA_Project_AaloLawrence_23CG034015

**Project:** AI-Powered Question Engine — Web GUI + CLI (Hugging Face Router API)

## Contents
- `LLM_QA_CLI.py` — CLI tool to ask questions to an LLM API
- `app.py` — Flask web GUI application
- `templates/index.html` — Web UI
- `static/style.css` — CSS for the UI
- `requirements.txt` — Python dependencies
- `Procfile` — For Render deployment (gunicorn)
- `LLM_QA_hosted_webGUI_link.txt` — add live URL after deploy

## Setup & Local Testing

1. Create a Python virtual env and install requirements:
```bash
python -m venv venv
source venv/bin/activate   # on Windows use: venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Set environment variables (example):
```bash
export HF_API_KEY="hf_YOUR_KEY"
export HF_MODEL="microsoft/DialoGPT-medium"
```

3. Run the Flask app:
```bash
python app.py
# open http://localhost:5000
```

4. Run the CLI tool:
```bash
python LLM_QA_CLI.py
```

## Deployment (Render)
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Set environment variables in Render (HF_API_KEY, optional HF_MODEL)
- Deploy and paste the live URL into `LLM_QA_hosted_webGUI_link.txt`

## Notes
- Do not commit your HF_API_KEY. Use env vars only.
- If encountering provider errors, check HF_MODEL name and HF_API_KEY validity.
