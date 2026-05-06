import os
import google.generativeai as genai

from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)


def load_prompt():
    with open(".github/prompts/review_prompt.txt", "r") as f:
        return f.read()


def format_code_context(context):
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

    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(prompt)

    return response.text