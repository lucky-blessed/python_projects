from github_activity.formatter import format_time_ago, format_event, format_events
from datetime import datetime, timezone, timedelta

def make_timestamp(seconds_ago: int) -> str:
    """
    Create an ISO 8601 UTC timestamp string for a time in the past.

    Args:
        seconds_ago: How many seconds in the past timestamp should be.

        Returns:
            An ISO 8601 formatted UTC timestamp string.
    """
    t = datetime.now(tz=timezone.utc) - timedelta(seconds=seconds_ago)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")

class TestFormatTimeAgo:
    """Tests for the format_time_ago function."""

    def test_seconds(self):
        ts = make_timestamp(30)
        assert format_time_ago(ts) == "30 seconds ago"

    def test_one_second(self):
        ts = make_timestamp(1)
        assert format_time_ago(ts) == "1 second ago"

    def test_minutes(self):
        ts = make_timestamp(60 * 5)
        assert format_time_ago(ts) == "5 minutes ago"

    def test_one_minute(self):
        ts = make_timestamp(60)
        assert format_time_ago(ts) == "1 minute ago"

    def test_hours(self):
        ts = make_timestamp(60 * 60 * 3)
        assert format_time_ago(ts) == "3 hours ago"

    def test_one_hour(self):
        ts = make_timestamp(60 * 60)
        assert format_time_ago(ts) == "1 hour ago"

    def test_days(self):
        ts = make_timestamp(60 * 60 * 24 * 5)
        assert format_time_ago(ts) == "5 days ago"

    def test_one_day(self):
        ts = make_timestamp(60 * 60 * 24)
        assert format_time_ago(ts) == "1 day ago"

    def test_months(self):
        ts = make_timestamp(60 * 60 * 24 * 60)
        assert format_time_ago(ts) == "2 months ago"

    def test_years(self):
        ts = make_timestamp(60 * 60 * 24 * 400)
        assert format_time_ago(ts) == "1 year ago"



class TestFormatEvent:
    """Tests for the format_event function."""

    def make_event(self, event_type: str, payload: dict = None) -> dict:
        """Build a minimal fake event dict for testing."""

        return {
            "type": event_type,
            "repo": {"name": "testuser/testrepo"},
            "payload": payload or {},
            "created_at": make_timestamp(3600), # 1 hour ago
        }
    
    def test_watch_event(self):
        event = self.make_event("WatchEvent")
        result = format_event(event)
        assert "Starred" in result
        assert "testuser/testrepo" in result

    def test_fork_event(self):
        event = self.make_event("ForkEvent", {
            "forkee": {"full_name": "otheruser/testrepo"}
        })
        result = format_event(event)
        assert "Forked" in result
        assert "testuser/testrepo" in result

    def test_issues_event_opened(self):
        event = self.make_event("IssuesEvent", {"action": "opened"})
        result = format_event(event)
        assert "Opened" in result
        assert "issue" in result

    def test_issues_event_closed(self):
        event = self.make_event("IssuesEvent", {"action": "closed"})
        result = format_event(event)
        assert "Closed" in result

    def test_create_event_branch(self):
        event = self.make_event("CreateEvent", {
            "ref_type": "branch",
            "ref": "feature/new-thing"
        })
        result = format_event(event)
        assert "Created" in result
        assert "branch" in result
        assert "feature/new-thing" in result

    def test_pull_request_event(self):
        event = self.make_event("PullRequestEvent", {
            "action": "opened",
            "pull_request": {"title": "Fix bug in api"}
        })
        result = format_event(event)
        assert "Opened" in result
        assert "Fix bug in api" in result

    def test_unknown_event(self):
        event = self.make_event("SomeNewEventType")
        result = format_event(event)
        assert "testuser/testrepo" in result

    def test_output_starts_with_dash(self):
        event = self.make_event("WatchEvent")
        result = format_event(event)
        assert result.startswith("- ")

    def test_timestamp_included(self):
        event = self.make_event("WatchEvent")
        result = format_event(event)
        assert "ago" in result


class TestFormatEvents:
    """Tests for format_events functions"""

    def test_empty_events(self):
        result =  format_events([])
        assert result == ["No recent public activity found."]

    def test_push_events_grouped(self):
        events = [
            {
                "type": "PushEvent",
                "repo": {"name": "testuser/repo-a"},
                "payload": {},
                "created_at": make_timestamp(100),
            },
            {
                
                "type": "PushEvent",
                "repo": {"name": "testuser/repo-a"},
                "payload": {},
                "created_at": make_timestamp(200),
            },
            {
                
                "type": "PushEvent",
                "repo": {"name": "testuser/repo-b"},
                "payload": {},
                "created_at": make_timestamp(300),
            },
        ]
        result = format_events(events)

        # Find push lines
        push_lines = [line for line in result if "Pushed" in line]
        assert len(push_lines) == 2 # repos, not 3 events

        repo_a_line = next(l for l in push_lines if "repo-a" in l)
        assert "2 times" in repo_a_line

        repo_b_line = next(l for l in push_lines if "repo-b" in l)
        assert "1 time" in repo_b_line

    def test_non_push_events_preserved(self):
        events = [
            {
                "type": "WatchEvent",
                "repo": {"name": "testuser/some-repo"},
                "payload": {},
                "created_at": make_timestamp(100),
            }
        ]
        result = format_events(events)
        assert  any("Starred" in line for line in result)


    def test_push_lines_prepended(self):
        events = [
            {
                "type": "WatchEvent",
                "repo": {"name": "testuser/repo"},
                "payload": {},
                "created_at": make_timestamp(100)
            },
            {
                "type": "PushEvent",
                "repo": {"name": "testuser/repo"},
                "payload": {},
                "created_at": make_timestamp(200)
            },
        ]
        result = format_events(events)
        # Push summary should appear before the Starred line
        push_index = next(i for i, l in enumerate(result) if "Pushed" in l)
        watch_index = next(i for i, l in enumerate(result) if "Starred" in l)
        assert push_index < watch_index