from __future__ import annotations
import sys
import argparse
from github_activity.api import fetch_user_activity
from github_activity.formatter import format_events


def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the CLI argument parser.

    Returns:
        A configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="github-activity",
        description="fetch and display recent public activity for a GitHub user.",
        epilog="Example: github-activity lucky-blessed",
    )

    parser.add_argument(
        "username",
        help="The GitHub username to fetch activity for.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Limit output to the N most recent events  (default: show all).",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    return parser

def main() -> None:
    """
    Main entry point for the github-activity CLI.

    Parses arguments, fetches GitHub activity, formats it, 
    and prints it to stdout.
    """
    parser = build_parser()
    args = parser.parse_args()

    username = args.username.strip()

    # Basic validation - GitHub username can't be empty or contain spaces
    if not username:
        print("Error: Username cannot be empty.")
        sys.exit(1)

    if " " in username:
        print(f"Error: '{username}' is not a valid GitHub username.")
        sys.exit(1)

    # Fetch activity from GitHub
    print(f"Fetching activity for '{username}'...\n")
    events = fetch_user_activity(username)

    # Appky limit if specified
    if args.limit is not None:
        events = events[:args.limit]

    # Format and print
    lines = format_events(events)
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()