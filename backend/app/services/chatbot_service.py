from openai import OpenAI
from app.core.config import settings
from app.services.memory_service import get_history, save_message
from app.services.vector_service import add, search

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_response(user_id, user_input):
    history = get_history(user_id)
    context = search(user_input)

    messages = [
        {"role": "system", "content": "You are a professional AI customer support assistant."}
    ]

    for m, r in reversed(history):
        messages.append({"role": "user", "content": m})
        messages.append({"role": "assistant", "content": r})

    if context:
        messages.append({
            "role": "system",
            "content": "Relevant past context:\n" + "\n".join(context)
        })

    messages.append({"role": "user", "content": user_input})

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = res.choices[0].message.content

    save_message(user_id, user_input, reply)
    add(user_input + " " + reply)

    return reply