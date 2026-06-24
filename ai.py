"""Shared Claude AI logic for workflow_builder."""

import json

import anthropic

SYSTEM_PROMPT = """\
You are a Python automation expert. The user will describe a repetitive task they want to automate.
Generate a ready-to-run Python script that automates it.

Return a JSON object with exactly two keys:
- "filename": A short, descriptive snake_case filename ending in .py (e.g. "rename_photos.py"). No path, just the filename.
- "script": The complete, ready-to-run Python script as a string. Use only the Python standard library unless the task clearly requires a third-party package. Include a brief comment at the top describing what the script does. Make it safe — no destructive operations without confirmation.

Return only valid JSON. No markdown fences, no extra text.
"""

MODEL = "claude-haiku-4-5-20251001"


def generate(task: str) -> dict:
    client = anthropic.Anthropic()

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": f"Task: {task}"}],
    )
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(raw)
