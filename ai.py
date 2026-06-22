"""Shared Gemini AI logic for workflow_builder."""

import json
import os

from google import genai
from google.genai import errors as genai_errors

SYSTEM_PROMPT = """\
You are a Python automation expert. The user will describe a repetitive task they want to automate.
Generate a ready-to-run Python script that automates it.

Return a JSON object with exactly two keys:
- "filename": A short, descriptive snake_case filename ending in .py (e.g. "rename_photos.py"). No path, just the filename.
- "script": The complete, ready-to-run Python script as a string. Use only the Python standard library unless the task clearly requires a third-party package. Include a brief comment at the top describing what the script does. Make it safe — no destructive operations without confirmation.

Return only valid JSON. No markdown fences, no extra text.
"""

MODELS = ["gemini-2.5-flash", "gemini-2.5-flash-lite"]


def generate(task: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in .env")

    client = genai.Client(api_key=api_key)

    for i, model in enumerate(MODELS):
        try:
            response = client.models.generate_content(
                model=model,
                contents=f"{SYSTEM_PROMPT}\n\nTask: {task}",
            )
            raw = response.text.strip()
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(raw)
        except genai_errors.ServerError as e:
            if "503" in str(e) and i < len(MODELS) - 1:
                continue
            raise
