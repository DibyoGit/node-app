import os
import requests

def post_comment(file_path, comment):
    repo = os.getenv("GITHUB_REPOSITORY") 
    pr_number = os.getenv("GITHUB_REF").split("/")[-1]
    token = os.getenv("GITHUB_TOKEN")

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    body = f"💡 **AI Review Suggestion for `{file_path}`**\n\n{comment}"
    response = requests.post(url, json={"body": body}, headers=headers)
    response.raise_for_status()
