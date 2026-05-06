import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_prompt():
    with open(".github/prompts/review_prompt.txt", "r") as f:
        return f.read()


def format_code_context(context):
    """
    Convert file context into readable format for LLM
    """
    formatted = []

    for file in context:
        formatted.append(
            f"\nFile: {file['file']} (Type: {file['type']})\n{file['content']}\n"
        )

    return "\n".join(formatted)


def build_prompt(ticket, context):
    template = load_prompt()

    return template.format(
        ticket_id=ticket["id"],
        ticket_type=ticket["type"],
        ticket_summary=ticket["summary"],
        ticket_description=ticket["description"],
        code_context=format_code_context(context)
    )


def analyze(ticket, context):
    prompt = build_prompt(ticket, context)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict code reviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content