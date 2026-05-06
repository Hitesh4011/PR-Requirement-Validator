import subprocess


def get_changed_files():
    files = []

    with open("files.txt", "r") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                change_type = parts[0]
                file_path = parts[-1]

                files.append({
                    "type": change_type,
                    "file": file_path
                })

    return files


def get_file_content(file_path):
    try:
        result = subprocess.run(
            ["git", "show", f"HEAD:{file_path}"],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception:
        return ""


def build_context():
    files = get_changed_files()
    context = []

    for f in files:
        if f["type"] == "D":
            context.append({
                "file": f["file"],
                "type": "DELETED",
                "content": "This file was deleted in this PR."
            })
            continue

        content = get_file_content(f["file"])

        context.append({
            "file": f["file"],
            "type": f["type"],
            "content": content[:2000]  # limit size
        })

    return context