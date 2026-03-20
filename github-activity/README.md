# github-activity

![CI](https://github.com/lucky-blessed/python_projects/actions/workflows/ci.yml/badge.svg)

A command line tool to fetch and display the recent public activity of any GitHub user directly in your terminal.

## Features

- View recent activity for any public GitHub user
- Groups push events by repository with occurrence counts
- Shows relative timestamps for all events (e.g. "2 hours ago")
- Supports limiting output with `--limit`
- Graceful error handling for invalid usernames and network issues

## Installation
```bash
pip install github-activity
```

## Usage
```bash
github-activity <username>
```

### Options

| Option | Description |
|--------|-------------|
| `--limit N` | Limit output to N most recent events |
| `--version` | Show the current version |
| `--help` | Show help message |

## Examples
```bash
# Fetch activity for a user
github-activity lucky-blessed

# Limit to 5 most recent events
github-activity lucky-blessed --limit 5
```

### Sample output
```
- Pushed 3 times to lucky-blessed/python_projects
- Pushed 9 times to lucky-blessed/nodejs-projects
- Starred lucky-blessed/alx-backend-python  [4 days ago]
```

## Development

### Prerequisites

- Python 3.8+
- Git

### Setup
```bash
git clone https://github.com/lucky-blessed/python_projects.git
cd python_projects/github-activity
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
pip install -e ".[dev]"
```

### Running tests
```bash
pytest tests/ -v
```

## Project structure
```
github-activity/
├── src/
│   └── github_activity/
│       ├── cli.py          # Entry point & argument parsing
│       ├── api.py          # GitHub API client
│       └── formatter.py    # Event formatting logic
├── tests/
│   ├── test_api.py
│   ├── test_cli.py
│   └── test_formatter.py
└── pyproject.toml
```

## License

MIT