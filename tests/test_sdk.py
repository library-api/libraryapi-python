"""
Live integration tests for the libraryapi Python SDK.

Run:
    LIBRARYAPI_TEST_KEY=sk_live_... pytest -v
"""
import os
import asyncio

import pytest

from libraryapi import (
    AsyncLibraryAPI,
    AuthenticationError,
    InvalidParamsError,
    LibraryAPI,
    NotFoundError,
)

API_KEY = os.environ.get("LIBRARYAPI_TEST_KEY")
pytestmark = pytest.mark.skipif(not API_KEY, reason="LIBRARYAPI_TEST_KEY env var required")


@pytest.fixture
def client():
    with LibraryAPI(api_key=API_KEY) as c:
        yield c


def test_health(client):
    body = client.health()
    assert body["db"] is True
    assert body["source"]["imls_year"] == "FY 2023"


def test_outlets_near_address(client):
    outlets = client.outlets.near(
        address="14901 Dale Evans Pkwy, Apple Valley, CA",
        radius_miles=10,
        limit=3,
    )
    assert len(outlets) >= 1
    top = outlets[0]
    assert "Apple Valley" in top.name
    assert top.fscs_id == "CA0109"
    assert top.distance_miles is not None and top.distance_miles < 1
    assert top.weekly_hours is not None


def test_outlets_near_coords(client):
    outlets = client.outlets.near(lat=34.5008, lng=-117.1825, radius_miles=5, limit=3)
    assert len(outlets) >= 1


def test_outlet_fetch(client):
    outlet = client.outlets.fetch("CA0109-004")
    assert outlet.outlet_id == "CA0109-004"
    assert outlet.geo and outlet.geo.lat


def test_library_fetch(client):
    sys = client.libraries.fetch("CA0109")
    assert sys.fscs_id == "CA0109"
    assert sys.service_area and sys.service_area.population > 1_000_000
    assert sys.finance and sys.finance.total_revenue > 0
    assert sys.collections and sys.collections.print_volumes > 0


def test_library_search(client):
    results = client.libraries.search(name="brooklyn", state="NY", limit=5)
    assert any("brooklyn" in (r.name or "").lower() for r in results)


def test_state_summary(client):
    ca = client.states.summary("CA")
    assert ca.state == "CA"
    assert ca.totals and ca.totals.library_systems > 100


def test_state_summary_invalid(client):
    with pytest.raises(InvalidParamsError):
        client.states.summary("CALIFORNIA")


def test_unknown_fscs_raises(client):
    with pytest.raises(NotFoundError):
        client.libraries.fetch("ZZ9999")


def test_bad_key_raises():
    with LibraryAPI(api_key="sk_live_DEFINITELY_BOGUS") as c:
        with pytest.raises(AuthenticationError):
            c.outlets.fetch("CA0109-004")


# ─────────────────────────── async ───────────────────────────

def test_async_outlets():
    async def go():
        async with AsyncLibraryAPI(api_key=API_KEY) as c:
            outlets = await c.outlets.near(address="14901 Dale Evans Pkwy, Apple Valley, CA", limit=1)
            assert outlets and outlets[0].fscs_id == "CA0109"

    asyncio.run(go())


def test_async_library_fetch():
    async def go():
        async with AsyncLibraryAPI(api_key=API_KEY) as c:
            sys = await c.libraries.fetch("CA0109")
            assert sys.fscs_id == "CA0109"

    asyncio.run(go())
