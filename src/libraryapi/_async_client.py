from __future__ import annotations

from typing import Optional

import httpx

from . import __version__
from ._http import _raise_for_error
from ._models import LibrarySystem, Outlet, StateSummary

BASE_URL = "https://api.libraryapi.dev"


class _AsyncOutletResource:
    def __init__(self, http: httpx.AsyncClient):
        self._http = http

    async def near(
        self,
        *,
        address: Optional[str] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius_miles: float = 10,
        limit: int = 10,
    ) -> list[Outlet]:
        params: dict = {"radius_miles": radius_miles, "limit": limit}
        if address:
            params["address"] = address
        if lat is not None:
            params["lat"] = lat
        if lng is not None:
            params["lng"] = lng
        resp = await self._http.get("/v1/outlets", params=params)
        _raise_for_error(resp)
        return [Outlet._from_dict(o) for o in resp.json()["data"]]

    async def fetch(self, outlet_id: str) -> Outlet:
        resp = await self._http.get(f"/v1/outlets/{outlet_id}")
        _raise_for_error(resp)
        return Outlet._from_dict(resp.json()["data"])


class _AsyncLibraryResource:
    def __init__(self, http: httpx.AsyncClient):
        self._http = http

    async def fetch(self, fscs_id: str) -> LibrarySystem:
        resp = await self._http.get(f"/v1/libraries/{fscs_id.upper()}")
        _raise_for_error(resp)
        return LibrarySystem._from_dict(resp.json()["data"])

    async def search(
        self,
        *,
        name: Optional[str] = None,
        state: Optional[str] = None,
        city: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[LibrarySystem]:
        params: dict = {"limit": limit, "offset": offset}
        if name:
            params["name"] = name
        if state:
            params["state"] = state
        if city:
            params["city"] = city
        resp = await self._http.get("/v1/libraries/search", params=params)
        _raise_for_error(resp)
        return [LibrarySystem._from_dict(d) for d in resp.json()["data"]]


class _AsyncStateResource:
    def __init__(self, http: httpx.AsyncClient):
        self._http = http

    async def summary(self, code: str) -> StateSummary:
        resp = await self._http.get(f"/v1/states/{code.upper()}/summary")
        _raise_for_error(resp)
        return StateSummary._from_dict(resp.json()["data"])


class AsyncLibraryAPI:
    """
    Asynchronous client for libraryapi.dev. Mirrors LibraryAPI's surface.

    Usage:
        import asyncio
        from libraryapi import AsyncLibraryAPI

        async def main():
            async with AsyncLibraryAPI(api_key="sk_live_...") as client:
                outlets = await client.outlets.near(address="...")
                print(outlets[0].name)

        asyncio.run(main())
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
        self._http = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers={
                "X-API-Key": api_key,
                "User-Agent": f"libraryapi-python/{__version__} async",
            },
        )
        self.outlets = _AsyncOutletResource(self._http)
        self.libraries = _AsyncLibraryResource(self._http)
        self.states = _AsyncStateResource(self._http)

    async def health(self) -> dict:
        resp = await self._http.get("/v1/health")
        _raise_for_error(resp)
        return resp.json()

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> "AsyncLibraryAPI":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()
