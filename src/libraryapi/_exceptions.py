class LibraryAPIError(Exception):
    """Base exception for all libraryapi errors."""

    def __init__(self, message: str, status_code: int | None = None, code: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code

    def __repr__(self) -> str:
        return f"{type(self).__name__}({super().__str__()!r}, status_code={self.status_code}, code={self.code!r})"


class AuthenticationError(LibraryAPIError):
    """401 — missing, invalid, or revoked API key."""


class QuotaExceededError(LibraryAPIError):
    """402 — monthly quota reached or prepaid balance empty."""


class NotFoundError(LibraryAPIError):
    """404 — library system / outlet not found, or no outlets in radius."""


class RateLimitError(LibraryAPIError):
    """429 — too many requests per minute."""


class InvalidParamsError(LibraryAPIError):
    """400 — invalid query parameters or unresolvable address."""
