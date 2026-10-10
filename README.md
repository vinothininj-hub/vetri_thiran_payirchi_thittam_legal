# LegalEase

AI-assisted legal document drafting application.

## Local setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
```

The included `.env` starts with `MOCK_AI=true`, so you can test without a Gemini key.

### Backend
```powershell
uvicorn backend.main:app --reload --port 8000
```
Open `http://127.0.0.1:8000/docs`.

### Frontend
In another terminal:
```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```
Open `http://localhost:8501`.

### Gemini
Edit `.env`:
```env
GEMINI_API_KEY=YOUR_REAL_API_KEY
GEMINI_MODEL=gemini-3.8-flash
MOCK_AI=false
```
Restart the backend.

### Docker
```powershell
docker compose up --build
```
Then open `http://localhost:8501`.

Generated documents are AI-assisted drafts, not legal advice, and should be reviewed by a qualified legal professional.
