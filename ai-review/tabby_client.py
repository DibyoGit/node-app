import json
import requests

TABBY_URL = "http://54.196.243.3:8080"
TABBY_AUTH_TOKEN = "auth_9675f108605f42f8bad46e5324d756ab"  # <-- your manual token

def get_tabby_review(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {TABBY_AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "Qwen2-1.5B-Instruct",
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }

    response = requests.post(f"{TABBY_URL}/v1/chat/completions",
                             headers=headers,
                             json=payload,
                             stream=True)

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
                print(f"⚠️ Error parsing chunk: {e}")

    return result.strip()
