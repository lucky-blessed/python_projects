import pytest
from unittest.mock import patch
from github_activity.cli import main, build_parser

FAKE_EVENTS = [
    {
        "type": "WatchEvent",
        "repo": {"name": "testuser/repo"},
        "payload": {},
        "created_at": "2026-01-01T10:00:00Z",
    },
]


class TestBuildParser:
    """Test for the argument parser."""

    def test_username_required(self):
        parser = build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_username_parsed(self):
        parser = build_parser()
        args = parser.parse_args(["lucky-blessed"])
        assert args.username == "lucky-blessed"

    def test_limit_parsed(self):
        parser = build_parser()
        args = parser.parse_args(["lucky-blessed", "--limit", "5"])
        assert args.limit == 5

    def test_limit_is_integer(self):
        parser = build_parser()
        args = parser.parse_args(["lucky-blessed", "--limit", "10"])
        assert isinstance(args.limit, int)

    def test_limit_default_is_none(self):
        parser = build_parser()
        args = parser.parse_args(["lucky-blessed"])
        assert args.limit is None



class TestMain:
    """Test for the main CLI function."""

    def test_fectches_and_prints(self, capsys):
        with patch("github_activity.cli.fetch_user_activity", return_value=FAKE_EVENTS):
            with patch("sys.argv", ["github-activity", "testuser"]):
                main()
            
        captured = capsys.readouterr()
        assert "testuser" in captured.out
        assert "Starred" in captured.out

    def test_invalid_username_with_space(self, capsys):
        with patch("sys.argv", ["github-activity", "invalid user"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1


    def test_limit_applied(self, capsys):
        many_events = FAKE_EVENTS * 10  # 10 identical events
        with patch("github_activity.cli.fetch_user_activity", return_value=many_events):
            with patch("sys.argv", ["github-activity", "testuser", "--limit", "3"]):
                main()

        captured = capsys.readouterr()
        assert "testuser" in captured.out
