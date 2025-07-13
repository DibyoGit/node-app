import os
import requests

def get_tabby_review(prompt: str) -> str:
    tabby_url = os.getenv("TABBY_URL", "http://localhost:8080")
    jwt_token = os.getenv("TABBY_API_TOKEN", "auth_9675f108605f42f8bad46e5324d756ab")

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "Qwen2-1.5B-Instruct",
        "stream": False,
        "messages": [
            { "role": "user", "content": prompt }
        ]
    }

    response = requests.post(f"{tabby_url}/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
