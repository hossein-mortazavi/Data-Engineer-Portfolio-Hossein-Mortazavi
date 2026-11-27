"""JSON structured logging with automatic redaction of sensitive fields.

Fields passed through ``extra={...}`` become top-level JSON keys, which keeps logs
queryable in Azure Monitor / Log Analytics, Loki or plain ``jq``.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import UTC, datetime
from typing import IO, Any

REDACTED = "***REDACTED***"
SENSITIVE_MARKERS = (
    "password",
    "passwd",
    "secret",
    "token",
    "api_key",
    "apikey",
    "authorization",
    "connection_string",
    "credential",
    "private_key",
)

# Attributes every LogRecord carries; anything else came from ``extra``.
_STANDARD_ATTRS = frozenset(
    logging.LogRecord("n", logging.INFO, "p", 0, "m", (), None).__dict__
) | {"message", "asctime", "taskName"}

_HANDLER_TAG = "_portfolio_handler"


def _is_sensitive(key: str) -> bool:
    lowered = key.lower()
    return any(marker in lowered for marker in SENSITIVE_MARKERS)


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: REDACTED if _is_sensitive(str(k)) else _redact(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_redact(v) for v in value]
    return value


class RedactingFilter(logging.Filter):
    """Replace values of sensitive-looking ``extra`` keys (including nested dict keys)."""

    def filter(self, record: logging.LogRecord) -> bool:
        for key in list(record.__dict__):
            if key in _STANDARD_ATTRS:
                continue
            record.__dict__[key] = (
                REDACTED if _is_sensitive(key) else _redact(record.__dict__[key])
            )
        return True


class JsonFormatter(logging.Formatter):
    """Render each record as a single-line JSON object."""

    def __init__(self, service: str = "portfolio") -> None:
        super().__init__()
        self.service = service

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "service": self.service,
            "message": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key not in _STANDARD_ATTRS:
                payload[key] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, ensure_ascii=False)


def configure_logging(
    level: str = "INFO",
    service: str = "portfolio",
    *,
    json_output: bool = True,
    stream: IO[str] | None = None,
) -> logging.Logger:
    """Configure the root logger once; calling again replaces the previous handler."""
    root = logging.getLogger()
    for handler in list(root.handlers):
        if getattr(handler, _HANDLER_TAG, False):
            root.removeHandler(handler)

    handler = logging.StreamHandler(stream or sys.stderr)
    setattr(handler, _HANDLER_TAG, True)
    handler.addFilter(RedactingFilter())
    if json_output:
        handler.setFormatter(JsonFormatter(service=service))
    else:
        handler.setFormatter(
            logging.Formatter(f"%(asctime)s %(levelname)s [{service}] %(name)s: %(message)s")
        )
    root.addHandler(handler)
    root.setLevel(level.upper())
    return root
