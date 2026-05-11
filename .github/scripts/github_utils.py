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


def format_result(result: dict):
    """
    Format LLM output (dict) into a professional Markdown report for PR readability.
    """
    status = result.get("status", "UNKNOWN").upper()
    summary = result.get("summary", "No summary provided.")
    issues = result.get("issues", [])

    # Map status to emojis
    emojis = {
        "APPROVED": "✅",
        "WARNING": "⚠️",
        "REJECTED": "❌"
    }
    emoji = emojis.get(status, "🔍")

    # Build the Markdown lines
    lines = [
        f"## 🤖 Automated PR Review: **{status}** {emoji}",
        "",
        "### 📝 Summary",
        summary,
        ""
    ]

    if issues:
        lines.append("### 🚩 Issues Found")
        for issue in issues:
            itype = issue.get("type", "ISSUE")
            msg = issue.get("message", "No details provided.")
            lines.append(f"- **[{itype}]**: {msg}")
        lines.append("")

    lines.append("---")
    lines.append("**Note:** This review is AI-generated. Please verify manually before merging.")

    return "\n".join(lines)