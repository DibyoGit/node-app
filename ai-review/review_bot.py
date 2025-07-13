import os
import requests
from tabby_client import get_tabby_review

# --- Config ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")  # e.g., "myuser/myrepo"
GITHUB_REF = os.getenv("GITHUB_REF", "")            # e.g., "refs/pull/42/merge"
TABBY_URL = os.getenv("TABBY_URL", "http://54.196.243.3:8080")


def get_pull_request_number():
    """
    Extract the pull request number from GITHUB_REF (e.g. "refs/pull/42/merge").
    """
    try:
        return GITHUB_REF.split("/")[2]
    except IndexError:
        raise RuntimeError(f"❌ Cannot extract PR number from GITHUB_REF='{GITHUB_REF}'")


def get_changed_files(pr_number):
    """
    Fetch the list of changed files in the PR using GitHub API.
    """
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{pr_number}/files"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    files = response.json()
    return [f["filename"] for f in files if f["filename"].endswith((".py", ".js", ".ts", ".java", ".go", ".rb"))]


def post_comment(pr_number, body):
    """
    Post a comment on the pull request.
    """
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.post(url, headers=headers, json={"body": body})
    response.raise_for_status()


def main():
    pr_number = get_pull_request_number()
    print(f"🔍 Pull Request #{pr_number}")

    changed_files = get_changed_files(pr_number)
    if not changed_files:
        print("✅ No code files changed. Skipping review.")
        return

    print(f"📂 Changed files: {changed_files}")

    for file_path in changed_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

            prompt = f"Please review and suggest improvements for the following code:\n\n{code}"
            suggestion = get_tabby_review(prompt, tabby_url=TABBY_URL)

            comment_body = f"💡 **AI Review Suggestion for `{file_path}`**\n\n{suggestion}"
            post_comment(pr_number, comment_body)
            print(f"✅ Comment posted for `{file_path}`")

        except Exception as e:
            print(f"⚠️ Skipping `{file_path}` due to error: {e}")


if __name__ == "__main__":
    main()
