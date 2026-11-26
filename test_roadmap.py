from services.nebius import ask_nebius
from services.prompts import load_prompt


student_profile = """
Name: Alex Johnson
Major: Computer Science
Concentration: Artificial Intelligence
Graduation Year: 2027
Career Goal: Work as an AI Product Manager
Technical Skills: Python, SQL, Machine Learning, APIs
Experience: One software engineering internship
Projects: AI chatbot for students
Research: No formal research experience
Leadership: Computer Science club member
"""

career_requirements = """
Target Role: AI Product Manager

Key Requirements:
- Product management fundamentals
- AI/ML understanding
- Technical communication
- User research
- Product analytics
- Agile development
- Experience working with engineering teams
- Strong communication and leadership
- Internship or project experience
"""

career_archetype = """
Common AI Product Manager Career Archetypes:

1. Technical Builder → Product Manager
- Starts with software engineering or technical projects
- Develops product sense through projects and internships
- Moves into product-focused internships or associate PM roles

2. AI/Research → Product
- Builds strong AI/ML knowledge
- Participates in research or AI projects
- Develops product and communication skills
- Transitions into AI product roles

Student Alignment:
- Strong technical foundation
- Some internship experience
- Has an AI project
- Needs more product management experience
- Needs stronger product portfolio and user research experience
"""

gap_analysis = """
Critical Gaps:
- No direct product management internship
- Limited product portfolio

High Priority:
- Product management fundamentals
- User research
- Product analytics
- Product case interview preparation

Medium Priority:
- Leadership experience
- Networking with product managers
- Additional AI product project
"""


graduation_date = "May 2027"


prompt = load_prompt(
    "roadmap.txt",
    {
        "student_profile": student_profile,
        "target_role": "AI Product Manager",
        "career_requirements": career_requirements,
        "career_archetype": career_archetype,
        "gap_analysis": gap_analysis,
        "current_date": "September 20, 2026",
        "graduation_date": graduation_date,
    }
)


result = ask_nebius(prompt)

print("\n===== ROADMAP =====\n")
print(result)