import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables
load_dotenv()

api_key = os.getenv("NEBIUS_API_KEY")
base_url = os.getenv("NEBIUS_BASE_URL")
model = os.getenv("NEBIUS_MODEL")

if not api_key:
    raise ValueError("NEBIUS_API_KEY is missing from .env")

if not base_url:
    raise ValueError("NEBIUS_BASE_URL is missing from .env")

if not model:
    raise ValueError("NEBIUS_MODEL is missing from .env")


# Find project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

prompt_path = PROJECT_ROOT / "prompts" / "cv_analysis.txt"
cv_path = PROJECT_ROOT / "backend" / "test_cv.txt"


# Read prompt
prompt_template = prompt_path.read_text(encoding="utf-8")


# Read CV
cv_text = cv_path.read_text(encoding="utf-8")


# Insert CV into prompt
prompt = prompt_template.replace("{{cv_text}}", cv_text)


# Connect to Nebius
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)


print("Sending CV to Nemotron...")
print()


response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.1
)


result = response.choices[0].message.content


print("===== NEMOTRON RESPONSE =====")
print()
print(result)