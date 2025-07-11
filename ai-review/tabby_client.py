import requests

def get_tabby_review(prompt: str, tabby_url="http://54.196.243.3:8080") -> str:
    """
    Sends a prompt to the TabbyML chat model and returns the response.
    
    Args:
        prompt (str): The prompt text to analyze.
        tabby_url (str): Base URL of the TabbyML server.
    
    Returns:
        str: AI-generated response from TabbyML.
    """
    try:
        response = requests.post(
            f"{tabby_url}/v1/chat/completions",
            json={
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.4,
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to communicate with TabbyML: {e}")
        return "⚠️ Error: Unable to connect to TabbyML server."
