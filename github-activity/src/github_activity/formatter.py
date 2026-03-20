from __future__ import annotations
from datetime import datetime, timezone

# Map GitHub event types to human readable verbs
EVENT_LABELS = {
    "PushEvent": "Pushed",
    "IssuesEvent": "Issue",
    "WatchEvent": "Starred",
    "ForkEvent": "Forked",
    "CreateEvent": "Created",
    "DeleteEvent": "Deleted",
    "PullRequestEvent": "Pull request",
    "IssueCommentEvent": "Commented on an issue in",
    "PublicEvent": "Made public",
    "MemberEvent": "Member event in"
}

def format_time_ago(iso_timestamp: str) -> str:
    """
    Convert an ISO 8601 timestamp into a human-friendly relative string.

    Example:
        "2026-01-15T10:30:00Z" -> "2hrs ago"

    Args:
        iso_timestamp: A UTC timestamp string in ISO 8601 format.

    Returns:
        A relative time string like '5 minutes ago' or  '3 days ago'
    """
    # Parse the ISO string into a datetime object
    event_time = datetime.strptime(iso_timestamp, "%Y-%m-%dT%H:%M:%SZ")

    # Make it timezone-aware (UTC) so we can compare it to now
    event_time = event_time.replace(tzinfo=timezone.utc)

    # Get the current time in UTC
    now = datetime.now(tz=timezone.utc)

    # Calculate the difference
    delta = now - event_time
    seconds = int(delta.total_seconds())

    if seconds < 60:
        return f"{seconds} second{'s' if seconds != 1 else ''} ago"
    
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    
    days = hours // 24
    if days < 30:
        return f"{days} day{'s' if days != 1 else ''} ago"
    
    months = days // 30
    if months < 12:
        return f"{months} month{'s' if months != 1 else ''} ago"
    
    years = days // 365
    return f"{years} year{'s' if years != 1 else ''} ago"


def format_event(event: dict) -> str:
    """
    Format a single GitHub event dictionary into a human readable string

    Args:
        Event: A single event dict from the GitHub API.

    Returns:
        A formatted string describing the event.         
    """
    event_type = event.get("type", "UnknownEvent")
    repo_name = event.get("repo", {}).get("name", "unknown/repo")
    payload = event.get("payload", {})
    created_at = event.get("created_at", "")

    time_ago = format_time_ago(created_at) if created_at else ""
    label = EVENT_LABELS.get(event_type, "Unknown event")


    if event_type == "PushEvent":
        # PushEvents are handled and grouped in format_events()
        # This is a fallback in case format_event is called directly
        message = f"Pushed to {repo_name}"

    elif event_type == "IssuesEvent":
        action = payload.get("action", "interacted with")
        message = f"{action.capitalize()} an issue in {repo_name}"

    elif event_type == "IssueCommentEvent":
        message = f"Commented on an issue in {repo_name}"

    elif event_type == "WatchEvent":
        message = f"Starred {repo_name}"

    elif event_type == "ForkEvent":
        forkee = payload.get("forkee", {}).get("full_name", "unknown/repo")
        message = f"Forked {repo_name} -> {forkee}"

    elif event_type == "CreateEvent":
        ref_type = payload.get("ref_type", "repository")
        ref = payload.get("ref") or repo_name
        message = f"Created {ref_type} '{ref}' in {repo_name}"

    elif event_type == "DeleteEvent":
        ref_type = payload.get("ref_type", "branch")
        ref = payload.get("ref", "unknown")
        message = f"Deleted {ref_type} '{ref}' in {repo_name}"

    elif event_type == "PullRequestEvent":
        action = payload.get("action", "interacted with")
        pr_title = payload.get("pull_request", {}).get("title", "a pull request")
        message = f"{action.capitalize()} PR: '{pr_title}' in {repo_name}"

    elif event_type == "PublicEvent":
        message = f"Made {repo_name} public"

    elif event_type == "MemberEvent":
        action = payload.get("action", "updated")
        member = payload.get("member", {}).get("login", "someone")
        message = f"{action.capitalize()} {member} as collaborator in {repo_name}" 

    else:
        message = f"{label} in {repo_name}"

    # Append relative time if available
    if time_ago:
        return f"- {message} [{time_ago}]"
    return f"- {message}"


def format_events(events: list[dict]) -> list[str]:
    """
    Format a list of GitHub events into human readable strings.

    PushEvents are grouped by repo and counted separetely, then prepended to the
    results list. All other events are formatted individually in the order they appear.

    Args:
        events: List of event dicts from the GitHub API.

    Returns:
        A list of formatted strings, one per event (pushes grouped by repo).
    """

    if not events:
        return ["No recent public activity found."]

    push_counts = {}  # { repo_name: count }
    results = []

    for event in events:
        if event.get("type") == "PushEvent":
            repo_name = event.get("repo", {}).get("name", "unknown/repo")
            # If we've seen this repo before, increament. Otherwise start at 1.
            push_counts[repo_name] = push_counts.get(repo_name, 0) + 1
        else:
            results.append(format_event(event))

    # Prepend push summaries to the top of the results
    for repo_name, count in push_counts.items():
        noun = "time" if count == 1 else "times"
        results.insert(0, f"- Pushed {count} {noun} to {repo_name}")

    return results