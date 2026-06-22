# workflow_builder

A Python CLI tool that turns a plain-English description of a repetitive task into a ready-to-run Python script. The script is displayed in the terminal with syntax highlighting, saved to the `workflows/` folder, and optionally executed immediately.

## How it works

1. Describe a repetitive task in plain English
2. The AI generates a complete Python script to automate it
3. The script is displayed with syntax highlighting
4. It's saved to `workflows/<descriptive_name>.py`
5. You're asked: **Run this now? (y/n)**

## Requirements

- Python 3.12+
- A free Gemini API key from [aistudio.google.com](https://aistudio.google.com)

## Setup

```bash
git clone https://github.com/petetorres375-glitch/workflow-builder.git
cd workflow_builder

pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your Gemini API key
```

## Usage

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

## Project Structure

```
workflow_builder/
├── main.py           — CLI entry point
├── requirements.txt
├── .gitignore
├── README.md
├── workflows/        — generated scripts saved here
└── logs/
    └── sessions.log  — task and filename log (gitignored)
```
