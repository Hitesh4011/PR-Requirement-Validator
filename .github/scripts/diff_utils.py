import requests
import os

def get_pr_files():
    repo = os.getenv("REPO")
    pr_number = os.getenv("PR_NUMBER")
    token = os.getenv("GITHUB_TOKEN")

    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    return response.json()


def build_context():
    files = get_pr_files()
    context = []

    for f in files:
        context.append({
            "file": f.get("filename"),
            "type": f.get("status"),
            "content": f.get("patch", "")
        })

    print(context)

    return context