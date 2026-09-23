"""Tests for the TursoDB database module."""
import pytest
from unittest.mock import AsyncMock, Mock, patch

from src.database import Database


class TestInit:
    def test_init_stores_config(self):
        db = Database("libsql://test.turso.io", "test_token")
        assert db.url == "libsql://test.turso.io"
        assert db.token == "test_token"
        assert db.client is None

    def test_require_client_raises_before_initialize(self):
        db = Database("libsql://test.turso.io", "test_token")
        with pytest.raises(RuntimeError, match="not initialized"):
            db._require_client()


class TestQueries:
    def make_initialized_db(self) -> Database:
        db = Database("libsql://test.turso.io", "test_token")
        db.client = Mock()
        return db

    async def test_get_active_authorities_returns_dicts(self):
        db = self.make_initialized_db()
        row = {"id": "mtc-chennai", "name": "MTC Chennai", "active": 1}
        db.client.execute = AsyncMock(return_value=Mock(rows=[row]))

        authorities = await db.get_active_authorities()

        assert authorities == [row]
        sql = db.client.execute.call_args.args[0]
        assert "active = 1" in sql

    async def test_get_complaints_appends_limit_param(self):
        db = self.make_initialized_db()
        db.client.execute = AsyncMock(return_value=Mock(rows=[]))

        await db.get_complaints(authority_id="mtc-chennai", category="frequency")

        params = db.client.execute.call_args.args[1]
        assert params[0] is not None
        assert params[-1] == 50

    async def test_insert_complaint_awaits_execute(self):
        db = self.make_initialized_db()
        db.client.execute = AsyncMock()

        complaint_id = await db.insert_complaint({
            "x_post_id": "123",
            "content": "Bus late",
            "posted_at": "2026-03-11T08:00:00",
        })

        assert complaint_id
        db.client.execute.assert_awaited_once()
        sql = db.client.execute.call_args.args[0]
        assert "INSERT INTO complaints" in sql
