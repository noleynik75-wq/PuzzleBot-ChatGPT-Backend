from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

OPENAI_KEY = os.getenv("OPENAI_KEY")
PUZZLEBOT_TOKEN = os.getenv("PUZZLEBOT_TOKEN")

def ask_gpt(message):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_KEY}"}
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": message}]
    }
    r = requests.post(url, headers=headers, json=data)
    return r.json()["choices"][0]["message"]["content"]

@app.post("/puzzle")
async def puzzle_endpoint(request: Request):
    body = await request.json()

    user_text = body.get("message", "")

    reply = ask_gpt(user_text)

    requests.post(
        "https://api.puzzlebot.top/api/sendMessage",
        json={
            "token": PUZZLEBOT_TOKEN,
            "chat_id": body.get("chat_id"),
            "text": reply
        }
    )

    return {"status": "ok"}
