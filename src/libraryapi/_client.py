from __future__ import annotations

from typing import Optional

import httpx

from . import __version__
from ._http import _raise_for_error
from ._models import LibrarySystem, Outlet, StateSummary

BASE_URL = "https://api.libraryapi.dev"


class _OutletResource:
    def __init__(self, http: httpx.Client):
        self._http = http

    def near(
        self,
        *,
        address: Optional[str] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius_miles: float = 10,
        limit: int = 10,
    ) -> list[Outlet]:
        """Find the nearest public library outlets to an address or coordinate."""
        params: dict = {"radius_miles": radius_miles, "limit": limit}
        if address:
            params["address"] = address
        if lat is not None:
            params["lat"] = lat
        if lng is not None:
            params["lng"] = lng
        resp = self._http.get("/v1/outlets", params=params)
        _raise_for_error(resp)
        return [Outlet._from_dict(o) for o in resp.json()["data"]]

    def fetch(self, outlet_id: str) -> Outlet:
        """Fetch a single outlet by its compound id, e.g. 'CA0109-004'."""
        resp = self._http.get(f"/v1/outlets/{outlet_id}")
        _raise_for_error(resp)
        return Outlet._from_dict(resp.json()["data"])


class _LibraryResource:
    def __init__(self, http: httpx.Client):
        self._http = http

    def fetch(self, fscs_id: str) -> LibrarySystem:
        """Fetch a library system's full profile by its 6-character FSCSKEY (e.g. 'CA0109')."""
        resp = self._http.get(f"/v1/libraries/{fscs_id.upper()}")
        _raise_for_error(resp)
        return LibrarySystem._from_dict(resp.json()["data"])

    def search(
        self,
        *,
        name: Optional[str] = None,
        state: Optional[str] = None,
        city: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[LibrarySystem]:
        """Search library systems by name, state, and/or city."""
        params: dict = {"limit": limit, "offset": offset}
        if name:
            params["name"] = name
        if state:
            params["state"] = state
        if city:
            params["city"] = city
        resp = self._http.get("/v1/libraries/search", params=params)
        _raise_for_error(resp)
        return [LibrarySystem._from_dict(d) for d in resp.json()["data"]]


class _StateResource:
    def __init__(self, http: httpx.Client):
        self._http = http

    def summary(self, code: str) -> StateSummary:
        """State-level rollup for a 2-letter state code."""
        resp = self._http.get(f"/v1/states/{code.upper()}/summary")
        _raise_for_error(resp)
        return StateSummary._from_dict(resp.json()["data"])


class LibraryAPI:
    """
    Synchronous client for the libraryapi.dev REST API.

    Usage:
        from libraryapi import LibraryAPI

        client = LibraryAPI(api_key="sk_live_...")
        outlets = client.outlets.near(address="14901 Dale Evans Pkwy, Apple Valley, CA")
        print(outlets[0].name, outlets[0].distance_miles)

        system = client.libraries.fetch(outlets[0].fscs_id)
        print(system.serviceArea.population if system.service_area else "—")

    Args:
        api_key: Your libraryapi.dev API key. Get one free at https://libraryapi.dev/pricing.
        base_url: Override the API base URL (e.g. for staging).
        timeout: Per-request timeout in seconds (default 30).
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = BASE_URL,
        timeout: float = 30.0,
    ):
        if not api_key:
            raise ValueError("api_key is required. Get one at https://libraryapi.dev/pricing")
        self._http = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers={
                "X-API-Key": api_key,
                "User-Agent": f"libraryapi-python/{__version__}",
            },
        )
        self.outlets = _OutletResource(self._http)
        self.libraries = _LibraryResource(self._http)
        self.states = _StateResource(self._http)

    def health(self) -> dict:
        """Hit /v1/health. Does not require an API key and does not consume credits."""
        resp = self._http.get("/v1/health")
        _raise_for_error(resp)
        return resp.json()

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "LibraryAPI":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
