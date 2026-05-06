import requests
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


def extract_description(desc):
    """
    Jira description can be complex JSON → flatten it
    """

    if not desc:
        return ""

    # If already string
    if isinstance(desc, str):
        return desc

    text_parts = []

    try:
        for block in desc.get("content", []):
            for inner in block.get("content", []):
                if "text" in inner:
                    text_parts.append(inner["text"])
    except Exception:
        pass

    return " ".join(text_parts)