class LBCError(Exception):
    """Base exception for all errors raised by the LBC client."""

class InvalidValue(LBCError):
    """Raised when a provided value is invalid or improperly formatted."""

class RequestError(LBCError):
    """Raised when an HTTP request fails with a non-success status code."""

class DatadomeError(RequestError):
    """Raised when access is blocked by Datadome anti-bot protection."""

class NotFoundError(LBCError):
    """Raised when a user or ad is not found."""
