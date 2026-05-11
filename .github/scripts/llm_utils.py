import os
import json
from google import genai
import re
from config import GEMINI_API_KEY
import time

client = genai.Client(api_key=GEMINI_API_KEY)


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
    print(f"prompt: {prompt}")

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt,
            )
            print(f"we are getting response with {response}")

            try:
                text = response.text.strip()
            except ValueError:
                if response.candidates and response.candidates[0].finish_reason == "SAFETY":
                    return {
                        "status": "REJECTED",
                        "issues": [{
                            "type": "SAFETY_BLOCK",
                            "message": "The AI refused to review this code due to safety policy violations."
                        }],
                        "summary": "AI review was blocked by safety filters."
                    }
                raise

            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                return {
                    "status": "REJECTED",
                    "issues": [{
                        "type": "FORMAT_ERROR",
                        "message": "LLM did not return valid JSON"
                    }],
                    "summary": text[:300]
                }

            json_text = match.group(0)
            try:
                return json.loads(json_text)
            except Exception:
                return {
                    "status": "REJECTED",
                    "issues": [{
                        "type": "FORMAT_ERROR",
                        "message": "LLM did not return valid JSON"
                    }],
                    "summary": text[:500]
                }

        except Exception as e:
            if attempt < 2 and any(err in str(e).lower() for err in ["429", "500", "503", "timeout"]):
                time.sleep(2)
                continue
            raise e