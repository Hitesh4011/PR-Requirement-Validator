import os

from parser import extract_ticket_id
from jira_utils import get_ticket
from diff_utils import build_context
from llm_utils import analyze
from github_utils import post_comment, format_result


def main():
    # === Read ENV ===
    pr_title = os.getenv("PR_TITLE")
    branch_name = os.getenv("BRANCH_NAME")
    repo = os.getenv("REPO")
    pr_number = os.getenv("PR_NUMBER")

    # === Step 1: Extract Ticket ID ===
    ticket_id = extract_ticket_id(branch_name)

    if not ticket_id:
        post_comment(
            repo,
            pr_number,
            "❌ No ticket ID found in PR title or branch name. Please follow naming convention (e.g., PROJ-123)."
        )
        return

    # === Step 2: Fetch Jira Ticket ===
    ticket = get_ticket(ticket_id)

    print(ticket)

    if not ticket:
        post_comment(
            repo,
            pr_number,
            f"❌ Unable to fetch Jira ticket `{ticket_id}`. Check ticket ID or permissions."
        )
        return
    
    # check for ticket status
    allowed_status = ["in progress", "in review"]

    ticket_status = ticket["status"].lower()

    if ticket_status not in allowed_status:
        post_comment(
            repo,
            pr_number,
            f"❌ Ticket `{ticket['id']}` is in invalid status `{ticket['status']}`.\n\n"
            f"Allowed statuses: In Progress, In Review"
        )
        return

    # === Step 3: Build Code Context ===
    context = build_context()

    print(context)

    if not context or all(not f["content"] for f in context):
        post_comment(   
            repo,
            pr_number,
            "⚠ No code changes detected."
        )
        return

    # === Step 4: LLM Analysis ===
    try:
        result = analyze(ticket, context)
        print(result)
    except Exception as e:
        # Extract the exact error type and message from the AI model
        error_type = type(e).__name__
        error_message = str(e)
        
        print(f"Error Type: {error_type}")
        print(f"Error Message: {error_message}")

        # Convert the system error into a structured response so it uses the standard UI
        result = {
            "status": "FAILED",
            "issues": [{
                "type": f"SYSTEM_ERROR_{error_type.upper()}",
                "message": error_message
            }],
            "summary": "The AI service encountered a technical error and could not complete the review. Please try again later."
        }

    # === Step 5: Format & Post Result ===
    formatted = format_result(result)
    post_comment(repo, pr_number, formatted)


if __name__ == "__main__":
    main()