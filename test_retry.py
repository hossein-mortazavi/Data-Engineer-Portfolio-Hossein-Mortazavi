"""Tests for shared.utilities.retry."""

import unittest

from shared.common.errors import DataValidationError, TransientError
from shared.utilities import compute_backoff, retry


class ComputeBackoffTests(unittest.TestCase):
    def test_exponential_growth_without_jitter(self) -> None:
        delays = [compute_backoff(n, base_delay=1.0, jitter=0.0) for n in (1, 2, 3, 4)]
        self.assertEqual(delays, [1.0, 2.0, 4.0, 8.0])

    def test_capped_at_max_delay(self) -> None:
        self.assertEqual(compute_backoff(10, base_delay=1.0, max_delay=5.0, jitter=0.0), 5.0)

    def test_jitter_bounds(self) -> None:
        low = compute_backoff(1, base_delay=10.0, jitter=0.2, rng=lambda: 0.0)
        high = compute_backoff(1, base_delay=10.0, jitter=0.2, rng=lambda: 1.0)
        self.assertAlmostEqual(low, 8.0)
        self.assertAlmostEqual(high, 12.0)

    def test_invalid_attempt(self) -> None:
        with self.assertRaises(ValueError):
            compute_backoff(0)


class RetryDecoratorTests(unittest.TestCase):
    def test_succeeds_after_transient_failures(self) -> None:
        sleeps: list[float] = []
        calls = {"n": 0}

        @retry(max_attempts=4, base_delay=1.0, jitter=0.0, sleep=sleeps.append)
        def flaky() -> str:
            calls["n"] += 1
            if calls["n"] < 3:
                raise TransientError("try again")
            return "ok"

        self.assertEqual(flaky(), "ok")
        self.assertEqual(calls["n"], 3)
        self.assertEqual(sleeps, [1.0, 2.0])

    def test_reraises_after_max_attempts(self) -> None:
        sleeps: list[float] = []
        calls = {"n": 0}

        @retry(max_attempts=3, jitter=0.0, sleep=sleeps.append)
        def always_fails() -> None:
            calls["n"] += 1
            raise TransientError("nope")

        with self.assertRaises(TransientError):
            always_fails()
        self.assertEqual(calls["n"], 3)
        self.assertEqual(len(sleeps), 2)

    def test_non_retryable_error_propagates_immediately(self) -> None:
        sleeps: list[float] = []
        calls = {"n": 0}

        @retry(max_attempts=5, sleep=sleeps.append)
        def bad_data() -> None:
            calls["n"] += 1
            raise DataValidationError("bad")

        with self.assertRaises(DataValidationError):
            bad_data()
        self.assertEqual(calls["n"], 1)
        self.assertEqual(sleeps, [])

    def test_invalid_max_attempts(self) -> None:
        with self.assertRaises(ValueError):
            retry(max_attempts=0)


if __name__ == "__main__":
    unittest.main()
