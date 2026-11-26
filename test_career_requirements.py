import json

from services.nebius import ask_nebius
from services.prompts import load_prompt


student_profile = {
    "education": {
        "major": "Computer Science",
        "graduation_year": "2027"
    },
    "technical_skills": [
        "Python",
        "SQL",
        "React"
    ],
    "experience": [
        "Software Engineering Intern"
    ]
}

target_role = "AI Product Manager"


prompt = load_prompt(
    "career_requirements.txt",
    {
        "student_profile": json.dumps(student_profile, indent=2),
        "target_role": target_role,
        "role_research": ""
    }
)

result = ask_nebius(prompt)

print(result)