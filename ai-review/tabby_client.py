import requests
import os
from requests.auth import HTTPBasicAuth

def get_tabby_review(prompt: str, tabby_url=None) -> str:
    tabby_url = tabby_url or os.getenv("TABBY_URL", "http://localhost:8080")
    username = os.getenv("TABBY_USERNAME")
    password = os.getenv("TABBY_PASSWORD")

    try:
        response = requests.post(
            f"{tabby_url}/v1/chat/completions",
            json={
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.4,
            },
            timeout=30,
            auth=HTTPBasicAuth(username, password) if username and password else None
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print(f"Error:  Failed to communicate with TabbyML: {e}")
        return "⚠️ Error: Unable to connect to TabbyML server."
