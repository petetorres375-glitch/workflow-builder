#!/usr/bin/env python3
"""workflow_builder — Describe a repetitive task, get a ready-to-run Python script."""

import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from google import genai
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax

load_dotenv()

BASE_DIR = Path(__file__).parent
WORKFLOWS_DIR = BASE_DIR / "workflows"
LOG_DIR = BASE_DIR / "logs"
WORKFLOWS_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "sessions.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
)

console = Console()

SYSTEM_PROMPT = """\
You are a Python automation expert. The user will describe a repetitive task they want to automate.
Generate a ready-to-run Python script that automates it.

Return a JSON object with exactly two keys:
- "filename": A short, descriptive snake_case filename ending in .py (e.g. "rename_photos.py"). No path, just the filename.
- "script": The complete, ready-to-run Python script as a string. Use only the Python standard library unless the task clearly requires a third-party package. Include a brief comment at the top describing what the script does. Make it safe — no destructive operations without confirmation.

Return only valid JSON. No markdown fences, no extra text.
"""


def generate(task: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[red]GEMINI_API_KEY not set in .env[/red]")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    with console.status("Generating script...", spinner="dots"):
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=f"{SYSTEM_PROMPT}\n\nTask: {task}",
        )

    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    return json.loads(raw)


def save_script(filename: str, script: str) -> Path:
    path = WORKFLOWS_DIR / filename
    path.write_text(script, encoding="utf-8")
    return path


def run_script(path: Path) -> None:
    console.print(f"\n[dim]Running {path.name}...[/dim]\n")
    result = subprocess.run([sys.executable, str(path)], capture_output=False)
    if result.returncode == 0:
        console.print("\n[green]Script finished successfully.[/green]")
    else:
        console.print(f"\n[red]Script exited with code {result.returncode}.[/red]")


def main():
    console.print(Panel(
        "[bold]Workflow Builder[/bold]\nDescribe a repetitive task and get a ready-to-run Python script.",
        border_style="white",
    ))

    while True:
        try:
            task = Prompt.ask("\n[bold cyan]Describe your task[/bold cyan]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Bye.[/dim]")
            break

        if not task:
            continue

        if task.lower() in {"exit", "quit", "q"}:
            console.print("[dim]Bye.[/dim]")
            break

        result = generate(task)
        filename = result.get("filename", f"workflow_{datetime.now().strftime('%H%M%S')}.py")
        script = result.get("script", "")

        console.print(f"\n[bold]Generated:[/bold] {filename}\n")
        console.print(Syntax(script, "python", theme="monokai", line_numbers=True))

        path = save_script(filename, script)
        console.print(f"\n[green]Saved:[/green] {path}")

        logging.info("TASK: %s | FILE: %s", task, filename)

        run_it = Confirm.ask("\n[bold yellow]Run this now?[/bold yellow]")
        if run_it:
            run_script(path)
        else:
            console.print(f"[dim]Skipped. Script saved at {path}[/dim]")


if __name__ == "__main__":
    main()
