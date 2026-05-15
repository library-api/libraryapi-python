"""
libraryapi — Python SDK for the libraryapi.dev API

US public library facility, hours, services, and statistics data — sourced from
the federal IMLS Public Libraries Survey.

Usage:
    from libraryapi import LibraryAPI

    client = LibraryAPI(api_key="sk_live_...")
    outlets = client.outlets.near(address="14901 Dale Evans Pkwy, Apple Valley, CA")
    print(outlets[0].name, outlets[0].distance_miles)        # Newton T. Bass... 0.14

    system = client.libraries.fetch(outlets[0].fscs_id)
    print(system.service_area.population)                    # 1263869

Async:
    import asyncio
    from libraryapi import AsyncLibraryAPI

    async def main():
        async with AsyncLibraryAPI(api_key="sk_live_...") as client:
            outlets = await client.outlets.near(address="...")

    asyncio.run(main())

Docs:    https://libraryapi.dev/docs
GitHub:  https://github.com/library-api/libraryapi-python
"""

__version__ = "0.2.0"

from ._async_client import AsyncLibraryAPI
from ._client import LibraryAPI
from ._exceptions import (
    AuthenticationError,
    InvalidParamsError,
    LibraryAPIError,
    NotFoundError,
    QuotaExceededError,
    RateLimitError,
)
from ._models import (
    Address,
    Collections,
    Finance,
    GeoPoint,
    LibrarySystem,
    Locale,
    Outlet,
    OutletService,
    ParentSystem,
    Programs,
    ResponseMeta,
    ResponseSource,
    ServiceArea,
    StaffFTE,
    StateAverages,
    StateSummary,
    StateTotals,
    Technology,
    Usage,
)

__all__ = [
    "__version__",
    "LibraryAPI",
    "AsyncLibraryAPI",
    # Models
    "Outlet",
    "LibrarySystem",
    "StateSummary",
    "Address",
    "GeoPoint",
    "ParentSystem",
    "OutletService",
    "Locale",
    "ServiceArea",
    "Collections",
    "Programs",
    "Technology",
    "Usage",
    "StaffFTE",
    "Finance",
    "StateTotals",
    "StateAverages",
    "ResponseMeta",
    "ResponseSource",
    # Exceptions
    "LibraryAPIError",
    "AuthenticationError",
    "QuotaExceededError",
    "NotFoundError",
    "RateLimitError",
    "InvalidParamsError",
]
