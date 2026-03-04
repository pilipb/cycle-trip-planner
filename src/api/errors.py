"""Error handling utilities: map exceptions to user-friendly messages and error codes."""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

# Error codes for frontend handling
ERROR_CONFIG = "config_error"  # Missing API key, env vars
ERROR_VALIDATION = "validation_error"  # Invalid request (422)
ERROR_SESSION = "session_error"  # No pending question, invalid session
ERROR_NETWORK = "network_error"  # Timeout, connection failed
ERROR_SERVICE = "service_error"  # External API (ORS, etc.) failed
ERROR_UNKNOWN = "unknown"  # Unexpected error


def _is_config_error(exc: BaseException) -> bool:
    """Check if exception is due to missing/invalid configuration."""
    msg = str(exc).lower()
    return (
        "api_key" in msg
        or "environment variable" in msg
        or "openroute" in msg
        or "anthropic" in msg
    )


def _is_validation_error(exc: BaseException) -> bool:
    """Check if exception is a validation error."""
    return type(exc).__name__ == "ValidationError" or "validation" in str(exc).lower()


def _is_network_error(exc: BaseException) -> bool:
    """Check if exception is network-related."""
    name = type(exc).__name__
    msg = str(exc).lower()
    return (
        "timeout" in msg
        or "connection" in msg
        or "network" in msg
        or name in ("TimeoutException", "ConnectError", "RequestError")
    )


def normalize_exception(exc: BaseException) -> tuple[str, str]:
    """
    Map an exception to a user-friendly message and error code.
    Returns (message, code). Never exposes stack traces or internal paths.
    """
    code = ERROR_UNKNOWN
    message = "Something went wrong. Please try again."

    if _is_config_error(exc):
        code = ERROR_CONFIG
        if "openroute" in str(exc).lower() or "openroute_service" in str(exc).lower():
            message = (
                "Route planning is not configured. Add OPENROUTE_SERVICE_API_KEY to your .env file. "
                "Get a free key at https://openrouteservice.org/dev/#/signup"
            )
        elif "anthropic" in str(exc).lower():
            message = (
                "AI service is not configured. Add ANTHROPIC_API_KEY to your .env file."
            )
        else:
            message = "A required configuration is missing. Check your .env file and README for setup instructions."
    elif _is_validation_error(exc):
        code = ERROR_VALIDATION
        message = "Invalid request. Please provide a message or answer the pending question."
    elif _is_network_error(exc):
        code = ERROR_NETWORK
        message = "Network error. Please check your connection and try again."
    elif "no pending question" in str(exc).lower() or "session" in str(exc).lower():
        code = ERROR_SESSION
        message = "No pending question for this session. Send a new message instead."
    else:
        # Log full details server-side but never expose to client
        logger.exception("Unhandled exception in chat stream")

    return message, code


def error_payload(message: str, code: str) -> dict[str, Any]:
    """Build SSE error payload with type, message, and code."""
    return {"type": "error", "message": message, "code": code}
