"""Small, dependency-free helpers for reading configuration from the environment.

Configuration comes from environment variables so the same code runs locally
(``.env`` file), in CI (workflow variables) and in Azure (Key Vault references or
app settings). Secrets are never given defaults.
"""

from __future__ import annotations

import os
from collections.abc import MutableMapping
from pathlib import Path

from shared.common.errors import ConfigurationError

_TRUE = frozenset({"1", "true", "yes", "on"})
_FALSE = frozenset({"0", "false", "no", "off"})


def _parse_value(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    # Unquoted values may carry a trailing " # comment".
    return value.split(" #", 1)[0].rstrip()


def load_env_file(
    path: str | Path,
    *,
    override: bool = False,
    environ: MutableMapping[str, str] | None = None,
) -> dict[str, str]:
    """Load ``KEY=VALUE`` pairs from a dotenv-style file into ``environ``.

    Existing variables win unless ``override`` is true, so real environment
    configuration always takes precedence over a developer's local file. A missing
    file is not an error and returns an empty dict. Returns the pairs that were read.
    """
    target = os.environ if environ is None else environ
    file_path = Path(path)
    if not file_path.is_file():
        return {}

    loaded: dict[str, str] = {}
    for line_no, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("export "):
            stripped = stripped[len("export ") :]
        if "=" not in stripped:
            raise ConfigurationError(f"{file_path}:{line_no}: expected KEY=VALUE")
        key, raw_value = stripped.split("=", 1)
        key = key.strip()
        if not key:
            raise ConfigurationError(f"{file_path}:{line_no}: empty variable name")
        value = _parse_value(raw_value)
        loaded[key] = value
        if override or key not in target:
            target[key] = value
    return loaded


def get_str(
    name: str,
    default: str | None = None,
    *,
    required: bool = False,
    environ: MutableMapping[str, str] | None = None,
) -> str | None:
    """Return a string setting. Raises ``ConfigurationError`` if required and unset/empty."""
    source = os.environ if environ is None else environ
    value = source.get(name)
    if value is None or value == "":
        if required:
            raise ConfigurationError(f"Required environment variable {name} is not set")
        return default
    return value


def get_int(
    name: str,
    default: int | None = None,
    *,
    required: bool = False,
    environ: MutableMapping[str, str] | None = None,
) -> int | None:
    """Return an integer setting, raising ``ConfigurationError`` on malformed values."""
    value = get_str(name, None, required=required, environ=environ)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer, got {value!r}") from exc


def get_bool(
    name: str,
    default: bool = False,
    *,
    environ: MutableMapping[str, str] | None = None,
) -> bool:
    """Return a boolean setting (1/0, true/false, yes/no, on/off; case-insensitive)."""
    value = get_str(name, None, environ=environ)
    if value is None:
        return default
    lowered = value.strip().lower()
    if lowered in _TRUE:
        return True
    if lowered in _FALSE:
        return False
    raise ConfigurationError(f"{name} must be a boolean, got {value!r}")


def mask_secret(value: str | None, visible: int = 2) -> str:
    """Return a log-safe representation of a secret, keeping at most ``visible`` end characters."""
    if not value:
        return ""
    if len(value) <= visible * 2:
        return "*" * len(value)
    return f"{value[:visible]}{'*' * (len(value) - visible * 2)}{value[-visible:]}"
