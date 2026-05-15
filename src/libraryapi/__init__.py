"""
libraryapi — Python SDK for the libraryapi.dev API

This is a placeholder release (v0.1.0) to claim the package name on PyPI.
The real SDK will be published as v0.2.0 after the API launches.

Usage (coming in v0.2.0):
    from libraryapi import LibraryAPI

    client = LibraryAPI(api_key="sk_live_...")
    outlets = client.outlets.search(address="12865 Main St, Apple Valley, CA", radius_miles=10)
    print(outlets[0].name)  # → Apple Valley Branch Library

Docs:    https://libraryapi.dev/docs
GitHub:  https://github.com/library-api/libraryapi-python
"""

__version__ = "0.1.0"
__all__ = ["LibraryAPI"]


class LibraryAPI:
    """
    Client for the libraryapi.dev REST API.

    Not yet implemented. Publishing v0.1.0 to claim the package name.
    Real implementation ships as v0.2.0.

    Args:
        api_key: Your libraryapi.dev API key. Get one free at https://libraryapi.dev
    """

    def __init__(self, api_key: str):
        raise NotImplementedError(
            "libraryapi v0.1.0 is a placeholder release. "
            "The real SDK ships as v0.2.0 after the API launches. "
            "Follow @libraryapi on X or watch https://github.com/library-api/libraryapi-python "
            "for updates."
        )
