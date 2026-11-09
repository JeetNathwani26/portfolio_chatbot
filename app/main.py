from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .models import ChatRequest, ChatResponse
from .rate_limit import InMemoryRateLimiter
from .resume import build_system_instruction, load_resume_text
from .service import ChatService

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    resume_text = load_resume_text(settings.resume_path)
    app.state.chat_service = ChatService(settings.groq_api_key, settings.groq_model, build_system_instruction(resume_text))
    app.state.rate_limiter = InMemoryRateLimiter(settings.requests_per_minute)
    yield


app = FastAPI(title="Portfolio Resume Chatbot", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_methods=["POST"], allow_headers=["Content-Type"])


@app.post("/chat", response_model=ChatResponse)
async def chat(request: Request, payload: ChatRequest) -> ChatResponse:
    # `payload.messages` is the conversation sent by the frontend.
    # Limit its size (4 by default) so one request cannot send unlimited history.
    if len(payload.messages) > settings.max_messages:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Too many messages.")

    # Reject overly long individual messages before they are sent to Groq.
    # This controls API cost and avoids unusually large requests.
    if any(len(message.text) > settings.max_message_length for message in payload.messages):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="A message is too long.")

    # Identify the caller by IP address. If FastAPI has no client information,
    # use a safe fallback name so the rate limiter still works.
    client_id = request.client.host if request.client else "unknown"

    # Allow only a limited number of chat requests from this IP per minute.
    # `check` raises HTTP 429 automatically when the limit is reached.
    request.app.state.rate_limiter.check(client_id)

    # Groq's Python client is synchronous. Run it in a worker thread so this
    # async FastAPI route can continue serving other visitors while it waits.
    reply = await run_in_threadpool(request.app.state.chat_service.reply, payload.messages)
    return ChatResponse(reply=reply)
