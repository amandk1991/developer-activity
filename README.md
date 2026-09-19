# Developer Activity Journal

An automated developer activity journal powered by GitHub Actions.

## What it does

Every day, the workflow:

1. Selects a development category.
2. Selects an engineering activity.
3. Records the activity in JSON.
4. Updates the Markdown developer journal.
5. Creates a Git commit when the repository changes.
6. Pushes the update to GitHub.
7. Records the activity in the GitHub Actions run.

## Activity categories

- Backend
- Frontend
- DevOps
- Security
- Documentation
- Testing
- Architecture

## Repository structure

```text
developer-activity/
├── .github/
│   └── workflows/
│       └── daily-developer-log.yml
│
├── activity/
│   ├── daily-log.md
│   └── activity.json
│
├── scripts/
│   ├── generate_activity.py
│   └── activities.json
│
├── .gitignore
├── README.md
└── requirements.txt
