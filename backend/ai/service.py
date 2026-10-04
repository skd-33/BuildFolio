from pydantic import ValidationError
from .schema import ProjectKnowledge
from .providers import chat_json

SYSTEM = """You write a technical portfolio draft from project notes.
Return ONLY JSON. Fill every field using the project info. Do not leave fields empty if the info allows it.

Example input:
PROJECT: Line Follower Robot
DESCRIPTION: Robot follows a black line using IR sensors
COMPONENTS: Arduino Uno, IR sensor, L298N driver, DC motors

Example output:
{"summary":"A robot that follows a black line using IR sensors.",
"problem":"Manual guidance of small robots is slow and error-prone.",
"solution":"IR sensors detect the line and an Arduino steers the motors through a motor driver.",
"hardware":[{"value":"Arduino Uno","status":"confirmed","source":"tracker"},{"value":"IR sensor","status":"confirmed","source":"tracker"}],
"software":[{"value":"Arduino C++","status":"inferred","source":"tracker"}],
"architecture":[{"value":"IR sensor reads the line","status":"inferred","source":"tracker"},{"value":"Arduino decides direction","status":"inferred","source":"tracker"},{"value":"L298N drives the motors","status":"inferred","source":"tracker"}],
"challenges":[],"future_improvements":[]}

Rules:
- Use only the given project info. Never invent numbers or results.
- status: "confirmed" if stated, "inferred" if deduced, "unknown" if unclear.
- Only challenges and future_improvements may be empty.
- Plain text only."""

def build_context(project: dict, extracted_text: str = "") -> str:
    parts = [
        f"PROJECT: {project['name']}",
        f"DESCRIPTION: {project.get('description', '')}",
        "COMPONENTS: " + ", ".join(c["name"] for c in project.get("components", [])),
        "TASKS: " + "; ".join(
            f"{t.get('name') or t.get('title') or 'Task'} ({'done' if t.get('done') else 'todo'})"
            for t in project.get("tasks", [])
        ),
        f"NOTES: {project.get('notes', '')}",
    ]
    if extracted_text:
        parts.append("DOCUMENT TEXT (source: uploaded files):\n" + extracted_text[:6000])
    return "\n".join(parts)

def generate_knowledge(project: dict, extracted_text: str = "",
                       images_b64: list[str] | None = None) -> ProjectKnowledge:
    user = build_context(project, extracted_text)
    last_err = ""
    for _ in range(3):
        prompt = user if not last_err else f"{user}\n\nYour last output was not acceptable: {last_err}\nReturn valid, filled JSON only."
        raw = chat_json(SYSTEM, prompt, images_b64)
        try:
            k = ProjectKnowledge.model_validate_json(raw)
            if k.summary.strip() or k.solution.strip() or k.hardware:
                return k
            last_err = "All fields were empty. Fill them using the project info."
        except ValidationError as e:
            last_err = str(e)[:300]
    raise ValueError("AI returned invalid or empty output")
