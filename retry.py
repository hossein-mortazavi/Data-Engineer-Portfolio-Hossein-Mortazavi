"""Retry decorator with capped exponential backoff and jitter.

Only exceptions listed in ``retry_on`` are retried (``TransientError`` by default);
everything else propagates immediately so that bad data or bugs are never retried.
``sleep`` and ``rng`` are injectable to keep tests fast and deterministic.
"""

from __future__ import annotations

import functools
import logging
import random
import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

from shared.common.errors import TransientError

P = ParamSpec("P")
T = TypeVar("T")

logger = logging.getLogger(__name__)


def compute_backoff(
    attempt: int,
    *,
    base_delay: float = 0.5,
    multiplier: float = 2.0,
    max_delay: float = 30.0,
    jitter: float = 0.1,
    rng: Callable[[], float] = random.random,
) -> float:
    """Delay in seconds before retry number ``attempt`` (1-based).

    ``delay = min(max_delay, base_delay * multiplier**(attempt-1))`` with a symmetric
    relative jitter of +/- ``jitter``, never below zero.
    """
    if attempt < 1:
        raise ValueError("attempt must be >= 1")
    delay = min(max_delay, base_delay * multiplier ** (attempt - 1))
    factor = 1.0 + jitter * (2.0 * rng() - 1.0)
    return max(0.0, delay * factor)


def retry(
    *,
    max_attempts: int = 5,
    base_delay: float = 0.5,
    multiplier: float = 2.0,
    max_delay: float = 30.0,
    jitter: float = 0.1,
    retry_on: tuple[type[BaseException], ...] = (TransientError,),
    sleep: Callable[[float], None] = time.sleep,
    rng: Callable[[], float] = random.random,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorate a callable so failures in ``retry_on`` are retried up to ``max_attempts`` times.

    The final failure is re-raised unchanged.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            attempt = 1
            while True:
                try:
                    return func(*args, **kwargs)
                except retry_on as exc:
                    if attempt >= max_attempts:
                        raise
                    delay = compute_backoff(
                        attempt,
                        base_delay=base_delay,
                        multiplier=multiplier,
                        max_delay=max_delay,
                        jitter=jitter,
                        rng=rng,
                    )
                    logger.warning(
                        "retrying after failure",
                        extra={
                            "function": func.__name__,
                            "attempt": attempt,
                            "max_attempts": max_attempts,
                            "delay_seconds": round(delay, 3),
                            "error": repr(exc),
                        },
                    )
                    sleep(delay)
                    attempt += 1

        return wrapper

    return decorator
