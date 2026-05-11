import requests
import re
from config import JIRA_API_KEY, JIRA_EMAIL, JIRA_URL


def get_ticket(ticket_id: str):
    """
    Fetch Jira ticket details.

    Returns:
    {
        "id": "PROJ-123",
        "summary": "...",
        "description": "...",
        "type": "...",
        "status": "..."
    }
    """

    url = f"{JIRA_URL}/rest/api/3/issue/{ticket_id}"

    response = requests.get(
        url,
        auth=(JIRA_EMAIL, JIRA_API_KEY),
        headers={"Accept": "application/json"}
    )

    if response.status_code != 200:
        return None

    data = response.json()
    fields = data.get("fields", {})

    return {
        "id": ticket_id,
        "summary": fields.get("summary", ""),
        "description": extract_description(fields.get("description")),
        "type": fields.get("issuetype", {}).get("name", ""),
        "status": fields.get("status", {}).get("name", "")
    }


def extract_description(node):
    """
    Recursively extract text from Jira ADF (Atlassian Document Format),
    preserving structure like lists, headings, and tables in Markdown.
    """
    if not node:
        return ""

    if isinstance(node, str):
        return node

    parts = []

    def walk(n):
        if not n:
            return
        if isinstance(n, list):
            for item in n:
                walk(item)
            return

        ntype = n.get("type")

        # Text nodes
        if ntype == "text":
            parts.append(n.get("text", ""))

        # Structure nodes
        elif ntype == "paragraph":
            parts.append("\n")
            walk(n.get("content", []))
            parts.append("\n")
        elif ntype == "heading":
            level = n.get("attrs", {}).get("level", 1)
            parts.append("\n" + ("#" * level) + " ")
            walk(n.get("content", []))
            parts.append("\n")
        elif ntype == "bulletList" or ntype == "orderedList":
            parts.append("\n")
            walk(n.get("content", []))
            parts.append("\n")
        elif ntype == "listItem":
            parts.append("\n- ")
            walk(n.get("content", []))
        elif ntype == "table":
            parts.append("\n")
            walk(n.get("content", []))
            parts.append("\n")
        elif ntype == "tableRow":
            parts.append("\n| ")
            walk(n.get("content", []))
        elif ntype == "tableHeader" or ntype == "tableCell":
            walk(n.get("content", []))
            parts.append(" | ")
        elif ntype == "codeBlock":
            parts.append("\n```\n")
            walk(n.get("content", []))
            parts.append("\n```\n")
        elif ntype == "hardBreak":
            parts.append("\n")
        else:
            # Fallback for unknown types: just keep digging for content
            walk(n.get("content", []))

    walk(node)

    # Clean up:
    # 1. Join all parts
    text = "".join(parts)
    # 2. Collapse 3 or more newlines into 2 (one blank line)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 3. Trim whitespace
    return text.strip()