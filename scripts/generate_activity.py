import json
import random
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ACTIVITY_DIR = ROOT / "activity"
ACTIVITY_FILE = ACTIVITY_DIR / "activity.json"
LOG_FILE = ACTIVITY_DIR / "daily-log.md"
TASK_FILE = ROOT / "scripts" / "activities.json"

ACTIVITY_DIR.mkdir(exist_ok=True)

now = datetime.now(timezone.utc)

date = now.strftime("%Y-%m-%d")
timestamp = now.strftime("%Y-%m-%d %H:%M:%S UTC")

# Load activity catalog
with TASK_FILE.open("r", encoding="utf-8") as file:
    activities = json.load(file)

# Load existing history
if ACTIVITY_FILE.exists():
    try:
        with ACTIVITY_FILE.open("r", encoding="utf-8") as file:
            history = json.load(file)
    except json.JSONDecodeError:
        history = {}
else:
    history = {}

history.setdefault("days", [])

# Prevent duplicate entries
if any(entry["date"] == date for entry in history["days"]):
    print(f"Activity already exists for {date}")
    raise SystemExit(0)

# Select category and activity
category = random.choice(list(activities.keys()))
task = random.choice(activities[category])

entry = {
    "date": date,
    "timestamp": timestamp,
    "category": category,
    "task": task
}

history["days"].append(entry)
history["days"].sort(key=lambda item: item["date"])

history["last_updated"] = timestamp
history["total_entries"] = len(history["days"])

# Save JSON
with ACTIVITY_FILE.open("w", encoding="utf-8") as file:
    json.dump(history, file, indent=2)

# Create/update Markdown journal
if LOG_FILE.exists():
    content = LOG_FILE.read_text(encoding="utf-8")
else:
    content = "# Developer Activity Journal\n\n"

entry_markdown = (
    f"## {date}\n\n"
    f"- **Focus:** {category.title()}\n"
    f"- **Activity:** {task}\n"
    f"- **Recorded:** {timestamp}\n\n"
)

content += entry_markdown

LOG_FILE.write_text(content, encoding="utf-8")

# GitHub Actions output
github_output = os.environ.get("GITHUB_OUTPUT")

if github_output:
    with open(github_output, "a", encoding="utf-8") as output:
        output.write(f"category={category}\n")
        output.write(f"task={task}\n")
        output.write(f"date={date}\n")

print(f"Created activity for {date}")
print(f"Category: {category}")
print(f"Task: {task}")
