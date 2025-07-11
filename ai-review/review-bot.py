import os
import subprocess
from github_api import post_comment
from tabby_client import get_tabby_review

def get_changed_files():
    output = subprocess.check_output(["git", "diff", "--name-only", "origin/main...HEAD"])
    return output.decode().splitlines()

def main():
    tabby_url = os.getenv("TABBY_URL", "http://54.196.243.3:8080")
    changed_files = get_changed_files()

    for file_path in changed_files:
        with open(file_path, "r") as f:
            code = f.read()

        prompt = f"Review this code for issues:\n\n{code}"
        suggestion = get_tabby_review(prompt, tabby_url)
        post_comment(file_path, suggestion)

if __name__ == "__main__":
    main()
