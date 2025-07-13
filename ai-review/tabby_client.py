import requests

TABBY_URL = "http://54.196.243.3:8080/v1/chat/completions"
JWT_TOKEN = "auth_9675f108605f42f8bad46e5324d756ab"  # Replace with your current token

def get_tabby_completion(user_input):
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "Qwen2-1.5B-Instruct",
        "stream": False,  # unless you're streaming token-by-token
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post(TABBY_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        raise Exception(f"Tabby error {response.status_code}: {response.text}")
