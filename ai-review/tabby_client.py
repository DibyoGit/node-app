import requests

TABBY_URL = "http://54.196.243.3:8080/v1/chat/completions"
JWT_TOKEN = "auth_9675f108605f42f8bad46e5324d756ab"  # Replace with your actual token if it changes

def get_tabby_review(code_snippet: str) -> str:
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "Qwen2-1.5B-Instruct",
        "stream": False,
        "messages": [
            {"role": "user", "content": f"Please review the following code:\n\n{code_snippet}"}
        ]
    }

    response = requests.post(TABBY_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
