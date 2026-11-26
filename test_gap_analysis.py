from services.nebius import ask_nebius
from services.prompts import load_prompt


student_profile = """
Name: Alex
Major: Computer Science
Graduation Year: 2027
Year: Junior

Technical Skills:
Python, SQL, JavaScript, React, basic machine learning

Experience:
- Software Engineering Intern at a small startup
- Built a machine learning classification project
- Member of university AI club

Research:
No formal research experience

Leadership:
AI club project lead

Career Goal:
AI Product Manager
"""


target_role = "AI Product Manager"


career_requirements = """
Role Overview:
AI Product Managers work at the intersection of product management,
AI/ML, engineering, and business.

Important Skills:
- Product strategy
- AI/ML fundamentals
- User research
- Data analysis
- SQL
- Communication
- Product sense
- Technical understanding

Typical Experience:
- Product internships
- Technical internships
- AI/ML projects
- Product case studies
- Cross-functional project experience

Important Hiring Signals:
- Strong technical foundation
- Product thinking
- Ability to work with engineers
- Evidence of building products
- Communication and leadership
"""


career_archetype = """
Archetype 1:
Technical-to-Product
People begin with software engineering or technical experience,
then move toward product management.

Archetype 2:
AI/ML-to-Product
People develop strong AI/ML knowledge through projects or research,
then transition into AI-focused product roles.

Student Alignment:
The student has technical internship experience,
AI/ML project experience, and leadership experience.

Potential Gaps:
Limited formal product management experience,
limited user research experience,
limited product strategy experience.
"""


prompt = load_prompt(
    "gap_analysis.txt",
    {
        "student_profile": student_profile,
        "target_role": target_role,
        "career_requirements": career_requirements,
        "career_archetype": career_archetype,
    }
)


result = ask_nebius(prompt)

print("\n===== GAP ANALYSIS =====\n")
print(result)