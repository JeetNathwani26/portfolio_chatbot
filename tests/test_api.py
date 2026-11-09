from app.models import ChatRequest


def test_empty_messages_are_rejected():
    try:
        ChatRequest(messages=[])
    except ValueError:
        return
    raise AssertionError("Empty conversations must be rejected")


def test_blank_message_is_rejected():
    try:
        ChatRequest.model_validate({"messages": [{"role": "user", "text": "   "}]})
    except ValueError:
        return
    raise AssertionError("Blank messages must be rejected")
