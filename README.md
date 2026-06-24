# workflow_builder

A Python tool that turns a plain-English description of a repetitive task into a ready-to-run Python script. The script is displayed with syntax highlighting, saved to the `workflows/` folder, and available to download. Runs as a web app or from the command line.

## How it works

1. Describe a repetitive task in plain English
2. The AI generates a complete Python script to automate it
3. The script is displayed with syntax highlighting
4. It's saved to `workflows/<descriptive_name>.py`
5. Download it directly from the browser (web) or run it immediately (CLI)

## Requirements

- Python 3.12+
- An Anthropic API key from [console.anthropic.com](https://console.anthropic.com)

## Setup

```bash
git clone https://github.com/petetorres375-glitch/workflow-builder.git
cd workflow_builder

pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your Anthropic API key
```

## Usage

**Web app:**

```bash
python app.py
```

Open `http://localhost:5052`, describe your task, and download the generated script.

**CLI:**

```bash
python main.py
```

Type `exit` or `quit` to close.

## Example

```
Describe your task: Rename all .jpeg files in a folder to .jpg

Generated: rename_jpeg_to_jpg.py

  1  # Renames all .jpeg files in the current directory to .jpg
  2  import os
  3  ...

Saved: workflows/rename_jpeg_to_jpg.py
Run this now? [y/n]: y
```

## Model

Uses `claude-haiku-4-5-20251001` via the Anthropic API. The system prompt is cached on every request to reduce latency and cost.

## Project Structure

```
workflow_builder/
├── main.py           — CLI entry point
├── app.py            — Flask web interface
├── requirements.txt
├── .gitignore
├── README.md
├── workflows/        — generated scripts saved here
└── logs/
    └── sessions.log  — task and filename log (gitignored)
```

## Live Demo

[https://web-production-515d4.up.railway.app/](https://web-production-515d4.up.railway.app/)

## Deploy to Railway

1. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub repo**
2. Select this repository
3. Add environment variables: `ANTHROPIC_API_KEY` and `SECRET_KEY`
4. Railway detects the `Procfile` and deploys automatically
