import requests
import os
from requests.auth import HTTPBasicAuth

def get_tabby_review(prompt: str, tabby_url=None) -> str:
    tabby_url = tabby_url or os.getenv("TABBY_URL", "http://54.196.243.3:8080")
    username = os.getenv("TABBY_USERNAME")
    password = os.getenv("TABBY_PASSWORD")

    if not username or not password:
        print("⚠️ Missing TabbyML credentials. Set TABBY_USERNAME and TABBY_PASSWORD.")
        return "⚠️ Error: Missing credentials for TabbyML."

    try:
        response = requests.post(
            f"{tabby_url}/v1/chat/completions",
            json={
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.4,
            },
            timeout=30,
            auth=HTTPBasicAuth(username, password)
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to communicate with TabbyML: {e}")
        return "⚠️ Error: Unable to connect to TabbyML server."
