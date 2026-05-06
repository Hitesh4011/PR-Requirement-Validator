import requests
from config import GITHUB_TOKEN


def post_comment(repo: str, pr_number: str, message: str):
    """
    Post a comment on PR
    """

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.post(url, headers=headers, json={"body": message})

    return response.status_code


def format_result(result: str):
    """
    Format LLM output for better PR readability
    """

    return f"""
## 🤖 Automated PR Review

{result}

---
**Note:** This review is AI-generated. Please verify before merging.
"""