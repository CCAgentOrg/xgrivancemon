"""Tests for database module."""
import pytest
from unittest.mock import Mock, patch
from src.database import TursoDatabase


class TestTursoDatabase:
    """Test suite for TursoDatabase class."""

    def test_init_stores_config(self):
        """Should store database URL and auth token."""
        db = TursoDatabase(
            database_url="libsql://test.turso.io",
            auth_token="test_token"
        )
        assert db.database_url == "libsql://test.turso.io"
        assert db.auth_token == "test_token"

    @patch("src.database.requests.post")
    def test_insert_complaint_success(self, mock_post):
        """Should insert complaint successfully."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [{"rows_affected": 1}]}
        mock_post.return_value = mock_response

        db = TursoDatabase("libsql://test.turso.io", "token")
        result = db.insert_complaint({
            "id": "123",
            "text": "Test complaint",
            "handle": "@MtcChennai",
            "category": "frequency"
        })

        assert result is True

    @patch("src.database.requests.post")
    def test_get_stats_returns_dict(self, mock_post):
        """Should return stats as dictionary."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{
                "rows": [
                    {"total": 100, "responded": 75, "resolved": 30}
                ]
            }]
        }
        mock_post.return_value = mock_response

        db = TursoDatabase("libsql://test.turso.io", "token")
        stats = db.get_weekly_stats("@MtcChennai")

        assert "total" in stats
        assert stats["total"] == 100
