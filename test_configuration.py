"""Tests for shared.configuration (unittest style so they run under unittest and pytest)."""

import tempfile
import unittest
from pathlib import Path

from shared.common.errors import ConfigurationError
from shared.configuration import get_bool, get_int, get_str, load_env_file, mask_secret


class GetStrTests(unittest.TestCase):
    def test_returns_value(self) -> None:
        self.assertEqual(get_str("A", environ={"A": "x"}), "x")

    def test_default_when_missing_or_empty(self) -> None:
        self.assertEqual(get_str("A", "d", environ={}), "d")
        self.assertEqual(get_str("A", "d", environ={"A": ""}), "d")

    def test_required_raises(self) -> None:
        with self.assertRaises(ConfigurationError):
            get_str("A", required=True, environ={})


class GetIntBoolTests(unittest.TestCase):
    def test_int_parses_and_defaults(self) -> None:
        self.assertEqual(get_int("N", environ={"N": "42"}), 42)
        self.assertEqual(get_int("N", 7, environ={}), 7)

    def test_int_malformed_raises(self) -> None:
        with self.assertRaises(ConfigurationError):
            get_int("N", environ={"N": "4x"})

    def test_bool_variants(self) -> None:
        for raw in ("1", "true", "YES", "On"):
            self.assertTrue(get_bool("B", environ={"B": raw}))
        for raw in ("0", "false", "No", "OFF"):
            self.assertFalse(get_bool("B", environ={"B": raw}))
        self.assertTrue(get_bool("B", True, environ={}))

    def test_bool_malformed_raises(self) -> None:
        with self.assertRaises(ConfigurationError):
            get_bool("B", environ={"B": "maybe"})


class LoadEnvFileTests(unittest.TestCase):
    def _write(self, text: str) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / ".env"
        path.write_text(text, encoding="utf-8")
        return path

    def test_parses_comments_quotes_export_and_inline_comment(self) -> None:
        path = self._write(
            "# comment\n\nA=1\nexport B=\"two words\"\nC='x' \nD=val # trailing\nE=a=b\n"
        )
        env: dict[str, str] = {}
        loaded = load_env_file(path, environ=env)
        self.assertEqual(
            env, {"A": "1", "B": "two words", "C": "x", "D": "val", "E": "a=b"}
        )
        self.assertEqual(loaded, env)

    def test_existing_environment_wins_unless_override(self) -> None:
        path = self._write("A=file\n")
        env = {"A": "real"}
        load_env_file(path, environ=env)
        self.assertEqual(env["A"], "real")
        load_env_file(path, override=True, environ=env)
        self.assertEqual(env["A"], "file")

    def test_missing_file_is_empty(self) -> None:
        self.assertEqual(load_env_file("/nonexistent/.env", environ={}), {})

    def test_malformed_line_raises(self) -> None:
        path = self._write("not a pair\n")
        with self.assertRaises(ConfigurationError):
            load_env_file(path, environ={})


class MaskSecretTests(unittest.TestCase):
    def test_masking(self) -> None:
        self.assertEqual(mask_secret(None), "")
        self.assertEqual(mask_secret("abc"), "***")
        self.assertEqual(mask_secret("abcdefgh"), "ab****gh")


if __name__ == "__main__":
    unittest.main()
