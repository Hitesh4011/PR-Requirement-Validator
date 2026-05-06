import re

TICKET_PATTERN = r"[A-Z]+-\d+"


def extract_ticket_id(pr_title: str, branch_name: str) -> str:
    """
    Extract ticket ID from PR title or branch name.

    Priority:
    1. PR Title
    2. Branch Name
    """

    # 1. Try PR title
    if pr_title:
        match = re.search(TICKET_PATTERN, pr_title)
        if match:
            return match.group(0)

    # 2. Try branch name
    if branch_name:
        match = re.search(TICKET_PATTERN, branch_name)
        if match:
            return match.group(0)

    # 3. Not found
    return None