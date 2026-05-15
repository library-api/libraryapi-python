# libraryapi

[![PyPI](https://img.shields.io/pypi/v/libraryapi-sdk.svg)](https://pypi.org/project/libraryapi-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/libraryapi-sdk.svg)](https://pypi.org/project/libraryapi-sdk/)

Official Python SDK for [libraryapi.dev](https://libraryapi.dev) — US public library facility, hours, services, and statistics data from the federal IMLS Public Libraries Survey. **9,252 systems · 17,586 outlets · FY 2023.**

## Install

```bash
pip install libraryapi-sdk
```

> **Note on naming:** `libraryapi` is taken on PyPI by an unrelated project. The
> install name is `libraryapi-sdk`; the Python import name is `libraryapi`.

Requires Python 3.9+. Only dependency is `httpx`.

## Quickstart

```python
from libraryapi import LibraryAPI

client = LibraryAPI(api_key="sk_live_...")  # https://libraryapi.dev/pricing

# Nearest outlets to an address
outlets = client.outlets.near(
    address="14901 Dale Evans Pkwy, Apple Valley, CA",
    radius_miles=10,
)
for o in outlets:
    print(f"{o.distance_miles:.2f} mi  {o.name}  ({o.weekly_hours} hrs/wk)")

# Full parent-system profile (collections, usage, programs, finance)
system = client.libraries.fetch(outlets[0].fscs_id)
print(system.name)                              # San Bernardino County Library
print(system.service_area.population)           # 1,263,869
print(system.finance.total_revenue)             # 28,327,522
print(system.usage.programs.attendance_total)   # 166,411

# State-level rollup
ca = client.states.summary("CA")
print(ca.totals.library_systems, ca.totals.outlets)  # 186 1192
```

## Async

```python
import asyncio
from libraryapi import AsyncLibraryAPI

async def main():
    async with AsyncLibraryAPI(api_key="sk_live_...") as client:
        outlets = await client.outlets.near(address="350 Fifth Ave, New York, NY")
        for o in outlets:
            print(o.name)

asyncio.run(main())
```

## Errors

```python
from libraryapi import LibraryAPI, NotFoundError, RateLimitError, QuotaExceededError

try:
    client.libraries.fetch("ZZ9999")
except NotFoundError:
    print("library system not found")
except QuotaExceededError:
    print("monthly quota reached")
except RateLimitError:
    print("slow down — too many requests per minute")
```

Exception hierarchy: `LibraryAPIError` → {`AuthenticationError`, `InvalidParamsError`, `QuotaExceededError`, `NotFoundError`, `RateLimitError`}.

## API surface

| Method | Returns |
|---|---|
| `client.outlets.near(address=..., radius_miles=..., limit=...)` | `list[Outlet]` |
| `client.outlets.near(lat=..., lng=..., radius_miles=..., limit=...)` | `list[Outlet]` |
| `client.outlets.fetch(outlet_id)` | `Outlet` |
| `client.libraries.fetch(fscs_id)` | `LibrarySystem` |
| `client.libraries.search(name=..., state=..., city=..., limit=..., offset=...)` | `list[LibrarySystem]` |
| `client.states.summary(code)` | `StateSummary` |
| `client.health()` | `dict` |

## Convenience properties

- `Outlet.weekly_hours` — `round(annual_hours / weeks_open)`

## Links

- [libraryapi.dev](https://libraryapi.dev)
- [API reference](https://libraryapi.dev/docs)
- [Pricing](https://libraryapi.dev/pricing)
- [LLM-friendly reference](https://libraryapi.dev/llms.txt)
- [Status](https://libraryapi.dev/status)
- [GitHub](https://github.com/library-api/libraryapi-python)
