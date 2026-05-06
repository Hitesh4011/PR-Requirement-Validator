import os

def main():
    print("=== PR VALIDATION STARTED ===")

    # Read env variables passed from workflow
    pr_title = os.getenv("PR_TITLE")
    branch_name = os.getenv("BRANCH_NAME")
    repo = os.getenv("REPO")
    pr_number = os.getenv("PR_NUMBER")

    print(f"PR Title: {pr_title}")
    print(f"Branch: {branch_name}")
    print(f"Repo: {repo}")
    print(f"PR Number: {pr_number}")

    # Read diff file
    try:
        with open("diff.txt", "r") as f:
            diff = f.read()
            print("Diff file loaded successfully")
            print(f"Diff length: {len(diff)} characters")
    except Exception as e:
        print("Error reading diff:", str(e))

    print("=== SCRIPT COMPLETED ===")

if __name__ == "__main__":
    main()