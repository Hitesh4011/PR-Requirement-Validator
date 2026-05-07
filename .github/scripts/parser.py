import re

TICKET_PATTERN = r"[A-Z]+-\d+"


def extract_ticket_id(branch_name: str) -> str:
    """
    Extract ticket ID from branch name.
    """

    if branch_name:
        match = re.search(TICKET_PATTERN, branch_name)
        if match:
            return match.group(0)

    # 3. Not found
    return None