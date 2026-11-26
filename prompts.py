from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROMPT_DIR = PROJECT_ROOT / "prompts"


def load_prompt(filename, variables=None):
    path = PROMPT_DIR / filename

    prompt = path.read_text(encoding="utf-8")

    if variables:
        for key, value in variables.items():
            prompt = prompt.replace(
                "{{" + key + "}}",
                str(value)
            )

    return prompt