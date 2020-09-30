import pytest
from entry import app

"""Tests Quart routes and ensure they are processing input correctly.
"""


@pytest.fixture(name="app", scope="function")
async def _app():
    await app.startup()
    yield app
    await app.shutdown()


@pytest.mark.asyncio
async def test_index(app):
    test_client = app.test_client()
    resp = await test_client.get("/")

    assert resp.status_code == 200
