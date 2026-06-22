"""workflow_builder — Flask web interface."""

import logging
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file

from ai import generate

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

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    task = ""
    error = None
    saved_path = None

    if request.method == "POST":
        task = request.form.get("task", "").strip()
        if task:
            try:
                result = generate(task)
                filename = result.get("filename", f"workflow_{datetime.now().strftime('%H%M%S')}.py")
                result["filename"] = filename
                path = WORKFLOWS_DIR / filename
                path.write_text(result.get("script", ""), encoding="utf-8")
                saved_path = str(path)
                logging.info("WEB TASK: %s | FILE: %s", task, filename)
            except Exception as e:
                msg = str(e)
                if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                    error = "Daily request limit reached. Try again tomorrow."
                elif "503" in msg or "UNAVAILABLE" in msg:
                    error = "The AI model is temporarily unavailable. Try again in a moment."
                else:
                    error = "Something went wrong. Please try again."

    return render_template("index.html", task=task, result=result, error=error, saved_path=saved_path)


@app.route("/download/<filename>")
def download(filename):
    path = WORKFLOWS_DIR / filename
    if not path.exists() or not path.suffix == ".py":
        return "Not found", 404
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=5052)
