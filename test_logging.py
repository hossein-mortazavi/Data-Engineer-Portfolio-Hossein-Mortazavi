"""Tests for shared.logging."""

import io
import json
import logging
import unittest

from shared.logging import configure_logging
from shared.logging.structured import REDACTED


class StructuredLoggingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stream = io.StringIO()
        configure_logging("DEBUG", "unit-test", stream=self.stream)
        self.addCleanup(self._cleanup)

    def _cleanup(self) -> None:
        root = logging.getLogger()
        for handler in list(root.handlers):
            if getattr(handler, "_portfolio_handler", False):
                root.removeHandler(handler)

    def _records(self) -> list[dict]:
        return [json.loads(line) for line in self.stream.getvalue().splitlines()]

    def test_emits_json_with_extra_fields(self) -> None:
        logging.getLogger("demo").info("loaded", extra={"rows": 10})
        (record,) = self._records()
        self.assertEqual(record["message"], "loaded")
        self.assertEqual(record["level"], "INFO")
        self.assertEqual(record["service"], "unit-test")
        self.assertEqual(record["logger"], "demo")
        self.assertEqual(record["rows"], 10)
        self.assertIn("timestamp", record)

    def test_sensitive_keys_are_redacted_including_nested(self) -> None:
        logging.getLogger("demo").info(
            "connect",
            extra={"db_password": "hunter2", "options": {"api_key": "k", "host": "h"}},
        )
        (record,) = self._records()
        self.assertEqual(record["db_password"], REDACTED)
        self.assertEqual(record["options"], {"api_key": REDACTED, "host": "h"})
        self.assertNotIn("hunter2", self.stream.getvalue())

    def test_exception_is_included(self) -> None:
        try:
            raise ValueError("boom")
        except ValueError:
            logging.getLogger("demo").exception("failed")
        (record,) = self._records()
        self.assertIn("ValueError: boom", record["exception"])

    def test_reconfigure_does_not_duplicate_output(self) -> None:
        configure_logging("INFO", "unit-test", stream=self.stream)
        logging.getLogger("demo").info("once")
        self.assertEqual(len(self._records()), 1)


if __name__ == "__main__":
    unittest.main()
