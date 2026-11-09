# Implementation Guide

## 1. Prepare the API

```powershell
cd resume-chatbot-api
Copy-Item .env.example .env
```

Set `GROQ_API_KEY` in `.env`, then install and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

To enable the optional two-minute backend heartbeat, set `HEARTBEAT_URL` to
the deployed API health URL, for example
`https://your-api.example.com/health`. The task starts and stops with the
FastAPI process and does not run unless this value is configured.

Open `http://localhost:8000/docs` to test the API.

## 2. Run the portfolio locally

Create `my_portfolio/.env.local` with:

```dotenv
VITE_CHAT_API_URL=http://localhost:8000
```

Then run `npm run dev` in `my_portfolio`. The chat bubble is available after the intro completes.

## 3. Deploy

- Deploy `resume-chatbot-api` as a Python web service.
- Add `GROQ_API_KEY`, `ALLOWED_ORIGINS=https://portfolio-two-wheat-79.vercel.app`, and `resume.txt` to that service.
- Use `uvicorn app.main:app --host 0.0.0.0 --port $PORT` as the start command.
- Add `VITE_CHAT_API_URL=https://your-api.example.com` to the frontend host and redeploy it.

## 4. Verify

```powershell
pytest
```

Also ask a resume-based question, an unknown-information question, an empty message, and a message longer than 2,000 characters. The widget reports network failures without losing the conversation already on screen.
