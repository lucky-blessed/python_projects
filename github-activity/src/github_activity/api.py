from __future__ import annotations
import urllib.request  # to make http request
import urllib.error
import json             # to parse JSON text into python dictionaries and list
import sys              # to access sys.exit()

# --- Constant ---
BASE_URL = "https://api.github.com/users/{username}/events"


def fetch_user_activity(username: str) -> list[dict]:
    """
    Fetch recent public activity for a GitHub user.

    Args:
        username: The GitHub username to look up.

    Returns:
        A list of event dictionaries from the GitHub API.

    Raises:
        SystemExit: On network errorsm bad username, or API failures.
    """

    url = BASE_URL.format(username=username)

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "github-activity-cli"
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read()
            data = json.loads(raw)
            return data
        
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: GitHub user '{username}' not found.")
        elif e.code == 403:
            print("Error: Github API rate limit exceeded. Wait a few minutes and try again.")
        elif e.code == 401:
            print("Error: Unauthorized. Check your GitHub token if using one.")
        else:
            print(f"Error: GitHub API returned a status {e.code}.")
        sys.exit(1)

    except urllib.error.URLError as e:
        print(f"Error: Could not connect to GitHub. Check your internet connection. \nDetails: {e.reason}")
        sys.exit(1)