"""Tests for the cookie-based X collector module."""
import pytest
from unittest.mock import Mock, patch

from src.collector import XCollector


def make_collector() -> XCollector:
    return XCollector(auth_token="test_auth", csrf_token="test_csrf")


class TestXCollectorInit:
    def test_init_stores_cookies(self):
        collector = make_collector()
        assert collector.session.cookies.get("auth_token", domain=".x.com") == "test_auth"

    def test_init_sets_csrf_header(self):
        collector = make_collector()
        assert collector.session.headers["X-Csrf-Token"] == "test_csrf"


class TestSearchTweets:
    @patch("src.collector.requests.Session.get")
    def test_search_tweets_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "globalObjects": {
                "tweets": {
                    "1": {
                        "id_str": "1",
                        "full_text": "Bus 26 late by 40 minutes",
                        "created_at": "Wed Mar 11 08:00:00 +0000 2026",
                        "reply_count": 2,
                        "retweet_count": 1,
                        "favorite_count": 5,
                    }
                }
            }
        }
        mock_get.return_value = mock_response

        collector = make_collector()
        tweets = collector.search_tweets("to:@MtcChennai", "", "")

        assert len(tweets) == 1
        assert tweets[0]["id"] == "1"
        assert tweets[0]["content"] == "Bus 26 late by 40 minutes"
        assert tweets[0]["url"] == "https://x.com/i/status/1"
        assert tweets[0]["like_count"] == 5

    @patch("src.collector.requests.Session.get")
    def test_search_tweets_request_error_returns_empty(self, mock_get):
        mock_get.side_effect = RuntimeError("connection refused")

        collector = make_collector()
        assert collector.search_tweets("to:@MtcChennai", "", "") == []

    @patch("src.collector.requests.Session.get")
    def test_search_tweets_non_200_returns_empty(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response

        collector = make_collector()
        assert collector.search_tweets("to:@MtcChennai", "", "") == []


class TestAsyncSearch:
    @patch("src.collector.requests.Session.get")
    async def test_search_complaints_builds_query(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"globalObjects": {"tweets": {}}}
        mock_get.return_value = mock_response

        collector = make_collector()
        result = await collector.search_complaints("@MtcChennai", since_hours=24)

        assert result == []
        called_query = mock_get.call_args.kwargs["params"]["q"]
        assert called_query.startswith("to:@MtcChennai")
