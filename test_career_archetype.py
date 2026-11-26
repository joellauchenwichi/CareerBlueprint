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

career_research = """
Example career research:

Professional A:
Computer Science degree → Software Engineering Internship
→ Product internship → AI Product Manager.

Professional B:
Computer Science degree → Data Analyst
→ Product Analyst → Product Manager → AI Product Manager.

Professional C:
Engineering degree → ML Engineer
→ Technical Product Manager → AI Product Manager.
"""


prompt = load_prompt(
    "career_archetype.txt",
    {
        "student_profile": json.dumps(student_profile, indent=2),
        "target_role": target_role,
        "career_research": career_research
    }
)

result = ask_nebius(prompt)

print(result)