# Resume Chatbot Folder Structure

```text
resume-chatbot-api/
├── app/
│   ├── __init__.py              # Python package marker
│   ├── config.py                # Environment-backed application settings
│   ├── main.py                  # FastAPI app and HTTP endpoint
│   ├── models.py                # Request and response schemas
│   ├── rate_limit.py            # Small in-memory IP rate limiter
│   ├── resume.py                # Safe PDF loading and prompt construction
│   └── service.py               # Groq conversation adapter
├── tests/
│   └── test_api.py              # Endpoint validation tests
├── scripts/
│   └── extract_resume.py         # One-time PDF-to-text conversion utility
├── .env.example                 # Safe configuration template
├── .gitignore                   # Excludes secrets and local resume copy
├── ARCHITECTURE.md               # Responsibility and data-flow guide
├── IMPLEMENTATION.md             # Setup, integration, and deployment guide
├── requirements.txt              # Runtime dependencies
└── README.md                     # Quick-start entry point
```

`resume.txt` is intentionally not committed in this folder. Generate it from the local `resume.pdf` before starting the API.
