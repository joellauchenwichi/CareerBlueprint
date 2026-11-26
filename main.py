import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel

from auth import router as auth_router

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

# Connect to Nebius Token Factory.
api_key = os.getenv("NEBIUS_API_KEY")

client = None

if api_key:
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.tokenfactory.nebius.com/v1/",
    )


# Information received from the frontend.
class RoadmapRequest(BaseModel):
    name: str = ""
    major: str = ""
    year: str = ""
    gradYear: str = ""
    region: str = ""
    careerGoal: list[str] | str = ""
    age: str = ""
    school: str = ""
    country: str = ""


@app.get("/")
def home():
    return {"message": "Career Blueprint backend is running!"}


@app.post("/api/roadmap")
def create_roadmap(request: RoadmapRequest):
    if not api_key or client is None:
        raise HTTPException(
            status_code=500,
            detail="NEBIUS_API_KEY is missing. Check your backend .env file.",
        )

    student_info = {
        "name": request.name,
        "major": request.major,
        "current_year": request.year,
        "graduation_year": request.gradYear,
        "preferred_region": request.region,
        "career_goals": request.careerGoal,
    }

    prompt = f"""
You are the AI career advisor for Career Blueprint.

Create a personalized, realistic career roadmap for this student.

STUDENT INFORMATION:
{json.dumps(student_info, indent=2)}

Requirements:
1. Personalize the roadmap using the student's actual information.
2. Consider their current university year and graduation year.
3. Prioritize practical steps they can take while at university.
4. Include relevant skills, projects, internships, networking,
   and preparation for their target careers where appropriate.
5. Avoid generic advice. Explain what the student should actually do.
6. Do not invent the student's experience, qualifications, or achievements.
7. If information is missing, make reasonable suggestions without
   pretending the student has provided that information.
8. Return between 4 and 6 roadmap steps in chronological order.

Return ONLY valid JSON in this exact structure:

{{
  "roadmap": [
    {{
      "title": "A short title",
      "description": "A specific explanation of what the student should do."
    }}
  ]
}}
"""

    try:
        response = client.chat.completions.create(
            model="nvidia/Nemotron-3_5-Lightning",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a thoughtful, practical career advisor. "
                        "Return valid JSON matching the requested structure."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
            max_tokens=2000,
        )

        ai_text = response.choices[0].message.content

        if not ai_text:
            raise ValueError("The AI returned an empty response.")

        result = json.loads(ai_text)
        roadmap = result.get("roadmap")

        if not isinstance(roadmap, list) or not roadmap:
            raise ValueError("The AI response did not contain a valid roadmap.")

        return {
            "success": True,
            "message": "AI-generated roadmap created successfully!",
            "student": student_info,
            "roadmap": roadmap,
        }

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="The AI returned an invalid JSON response. Please try again.",
        )

    except Exception as error:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=502,
            detail=f"{type(error).__name__}: {error}",
        )