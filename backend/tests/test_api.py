
import asyncio
from httpx import AsyncClient
from main import app
import pytest
from sqlmodel import SQLModel, create_engine
import os

@pytest.mark.asyncio
async def test_list_prs_empty():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        r = await ac.get('/api/prs')
        assert r.status_code == 200
        assert isinstance(r.json(), list)

@pytest.mark.asyncio
async def test_create_and_analyze_pr(tmp_path):
    # create a PR via API and (if model exists) attempt analyze (may 404 if model missing)
    payload = {
        "title": "Test PR",
        "author": "tester",
        "lines_changed": 123,
        "files_changed": 3,
        "comments": 2,
        "tests_modified": True
    }
    async with AsyncClient(app=app, base_url='http://test') as ac:
        r = await ac.post('/api/prs', json=payload)
        assert r.status_code == 200
        data = r.json()
        assert "id" in data
        pr_id = data["id"]
        # analyze may return 404 if model not trained in CI environment; we accept 200 or 404
        r2 = await ac.get(f'/api/prs/{pr_id}/analyze')
        assert r2.status_code in (200, 404)
