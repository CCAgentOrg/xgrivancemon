"""Tests for X API collector module."""
import pytest
from unittest.mock import Mock, patch
from src.collector import XCollector


class TestXCollector:
    """Test suite for XCollector class."""

    def test_init_requires_bearer_token(self):
        """Collector should require bearer token."""
        with pytest.raises(ValueError):
            XCollector(bearer_token="")

    def test_init_stores_token(self):
        """Collector should store bearer token."""
        collector = XCollector(bearer_token="test_token")
        assert collector.bearer_token == "test_token"

    @patch("src.collector.requests.get")
    def test_fetch_complaints_success(self, mock_get):
        """Should return complaints on successful API call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"id": "1", "text": "Bus late", "author_id": "user1"}
            ],
            "meta": {"newest_id": "1"}
        }
        mock_get.return_value = mock_response

        collector = XCollector(bearer_token="test")
        result = collector.fetch_complaints("@MtcChennai", hours=1)

        assert len(result) == 1
        assert result[0]["text"] == "Bus late"

    @patch("src.collector.requests.get")
    def test_fetch_complaints_api_error(self, mock_get):
        """Should return empty list on API error."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response

        collector = XCollector(bearer_token="test")
        result = collector.fetch_complaints("@MtcChennai", hours=1)

        assert result == []

    def test_extract_route_numbers(self):
        """Should extract route numbers from text."""
        collector = XCollector(bearer_token="test")
        text = "Route 26 and 597A are delayed"
        routes = collector._extract_routes(text)
        assert "26" in routes
        assert "597A" in routes

    def test_categorize_complaint_frequency(self):
        """Should categorize frequency complaints."""
        collector = XCollector(bearer_token="test")
        text = "Bus not coming for 30 minutes"
        category = collector._categorize(text)
        assert category == "frequency"

    def test_categorize_complaint_infrastructure(self):
        """Should categorize infrastructure complaints."""
        collector = XCollector(bearer_token="test")
        text = "Bus stop has no shelter"
        category = collector._categorize(text)
        assert category == "infrastructure"
