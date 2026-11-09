# Clean Architecture

## Data flow

```text
React chat widget
  -> POST /chat
  -> FastAPI route (validation, size limit, rate limit)
  -> ChatService (Groq SDK boundary)
  -> Groq API

Resume PDF -> Resume loader -> system instruction -> ChatService
```

## Responsibilities

| Layer | Files | Responsibility |
| --- | --- | --- |
| Configuration | `config.py` | Loads non-secret defaults and environment variables. |
| API | `main.py`, `models.py` | Exposes HTTP, validates input, and returns safe errors. |
| Application | `service.py` | Converts conversation messages to Groq chat messages and requests a reply. |
| Infrastructure | `resume.py`, `rate_limit.py` | Reads the resume once at startup and applies local request throttling. |

## Guardrails

- The API key lives only in `GROQ_API_KEY`; it is never sent to the browser.
- The resume is loaded once during application lifespan startup. Startup fails clearly when it is missing or empty.
- The system instruction restricts answers to the resume, blocks prompt-instruction disclosure, and asks the model not to invent information.
- Requests accept at most 10 messages and 2,000 characters per message. Requests are rate limited per client IP.
- CORS accepts only the configured portfolio origins. Configure production origins explicitly with `ALLOWED_ORIGINS`.

## Extension points

Replace the in-memory limiter with Redis for multi-instance hosting, and add a persistent session store only if conversation history must survive a browser refresh.
