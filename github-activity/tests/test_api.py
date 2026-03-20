import json
import sys
import pytest
from unittest.mock import patch, MagicMock
from github_activity.api import fetch_user_activity

FAKE_EVENTS = [
    {
        "type": "PushEvent",
        "repo": {"name": "testuser/repo"},
        "payload": {},
        "created_at": "2026-01-01T10:00:00Z",
    },
    {
        "type": "WatchEvent",
        "repo": {"name": "testuser/repo"},
        "payload": {},
        "created_at": "2026-01-01T09:00:00Z",
    },
]

class TestFetchUserActivity:
    """Tests for the fetch_user_activity function."""

    def make_response(self, data: list) -> MagicMock:
        """
        Build a fake urllip response object that returns JSON data.

        Args:
            data: The list of events to return as JSON.

        Returns:
            A MagicMock that behaves like a urllib response.
        """
        mock_response       = MagicMock()
        mock_response.read.return_value = json.dumps(data).encode("utf-8")
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        return mock_response
    
    def test_returns_list_of_events(self):
        mock_response = self.make_response(FAKE_EVENTS) 

        with patch("urllib.request.urlopen", return_value=mock_response):
            result = fetch_user_activity("testuser")

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["type"] == "PushEvent"

    def test_correct_url_called(self):
        mock_response = self.make_response(FAKE_EVENTS)

        with patch("urllib.request.urlopen", return_value=mock_response) as mock_open:
            fetch_user_activity("testuser")
            call_args = mock_open.call_args[0][0]
            assert "testuser" in call_args.full_url

    def test_404_exits_with_error(self):
        import urllib.error
        http_error = urllib.error.HTTPError(
            url=None, code=404, msg="Not Found", hdrs=None, fp=None
        )

        with patch("urllib.request.urlopen", side_effect=http_error):
            with pytest.raises(SystemExit) as exc_info:
                fetch_user_activity("nonexistentuser999")
            assert exc_info.value.code == 1

    def test_403_exits_with_error(self):
        import urllib.error
        http_error = urllib.error.HTTPError(
            url=None, code=403, msg="Forbidden", hdrs=None, fp=None
        )

        with patch("urllib.request.urlopen",  side_effect=http_error):
            with pytest.raises(SystemExit) as exc_info:
                fetch_user_activity("testuser")
            assert exc_info.value.code == 1

    def test_network_error_exits(self):
        import urllib.error
        url_error = urllib.error.URLError(reason="No network")

        with patch("urllib.request.urlopen", side_effect=url_error):
            with pytest.raises(SystemExit) as exc_info:
                fetch_user_activity("testuser")
            assert exc_info.value.code == 1