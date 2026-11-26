import os
from dotenv import load_dotenv
from openai import OpenAI

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

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "Say hello and confirm that you are ready to help with a career-planning application."
        }
    ],
    temperature=0.2
)

print("\n===== NEBIUS RESPONSE =====\n")
print(response.choices[0].message.content)