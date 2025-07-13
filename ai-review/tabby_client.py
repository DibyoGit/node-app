import os
import requests

TABBY_URL = os.getenv("TABBY_URL", "http://localhost:8080")
TABBY_AUTH_TOKEN = os.getenv("TABBY_AUTH_TOKEN", "")  # Optional

def get_tabby_review(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json"
    }
    if TABBY_AUTH_TOKEN:
        headers["Authorization"] = f"Bearer {TABBY_AUTH_TOKEN}"

    payload = {
        "model": "Qwen2-1.5B-Instruct",  # or "StarCoder-1B" if Qwen2 fails
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": True  # ✅ Required to avoid the invalid args error
    }

    response = requests.post(
        f"{TABBY_URL}/v1/chat/completions",
        headers=headers,
        json=payload,
        stream=True  # ✅ Required to handle streaming properly
    )

    if response.status_code != 200:
        raise RuntimeError(f"Tabby Error: {response.status_code} - {response.text}")

    result = ""
    for line in response.iter_lines(decode_unicode=True):
        if line and line.startswith("data: "):
            chunk = line.removeprefix("data: ").strip()
            if chunk == "[DONE]":
                break
            try:
                json_chunk = json.loads(chunk)
                delta = json_chunk["choices"][0]["delta"]
                result += delta.get("content", "")
            except Exception as e:
                print("⚠️ Error parsing chunk:", e)
                continue

    return result.strip()
