from groq import Groq

from .models import Message


class ChatService:
    def __init__(self, api_key: str, model: str, system_instruction: str) -> None:
        self.client = Groq(api_key=api_key)
        self.model = model
        self.system_instruction = system_instruction

    def reply(self, messages: list[Message]) -> str:
        # Groq uses OpenAI-compatible chat messages. The resume instruction is
        # a system message, while recent messages preserve short-term context.
        chat_messages = [{"role": "system", "content": self.system_instruction}]
        chat_messages.extend(
            {"role": "assistant" if message.role == "model" else "user", "content": message.text}
            for message in messages
        )
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=chat_messages,
            # Low reasoning is sufficient for resume Q&A and minimizes delay.
            reasoning_effort="low",
            include_reasoning=False,
            max_completion_tokens=180,
        )
        return (completion.choices[0].message.content or "I couldn't form a response just now. Please try again.").strip()
