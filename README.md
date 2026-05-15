# libraryapi

Python SDK for [libraryapi.dev](https://libraryapi.dev) — US public library facility, hours, services, and statistics data API.

## Status

This is a `v0.1.x` placeholder release to reserve the package name. The SDK is not yet functional.

```python
# Coming in v0.2.0
from libraryapi import LibraryAPI

client = LibraryAPI(api_key="sk_live_...")
outlets = client.outlets.search(address="12865 Main St, Apple Valley, CA", radius_miles=10)
print(outlets[0].name)
```

## Installation

```bash
pip install libraryapi
```

## Links

- [libraryapi.dev](https://libraryapi.dev)
- [GitHub](https://github.com/library-api/libraryapi-python)
