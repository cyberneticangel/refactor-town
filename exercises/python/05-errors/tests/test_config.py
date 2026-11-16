import os
import tempfile
import unittest

from config import ConfigError, read_settings


class ConfigTests(unittest.TestCase):
    def write(self, text):
        fd, path = tempfile.mkstemp(suffix=".conf")
        with os.fdopen(fd, "w") as f:
            f.write(text)
        self.addCleanup(os.remove, path)
        return path

    def test_parses_types(self):
        path = self.write(
            "# server settings\n"
            "port = 8080\n"
            "host = example.com\n"
            "\n"
            "debug = yes\n"
            "verbose = False\n"
            "retries=-3\n"
            "motd = a = b\n"
        )
        self.assertEqual(read_settings(path), {
            "port": 8080, "host": "example.com", "debug": True,
            "verbose": False, "retries": -3, "motd": "a = b",
        })

    def test_empty_file(self):
        self.assertEqual(read_settings(self.write("")), {})

    def test_missing_file(self):
        with self.assertRaises(ConfigError) as ctx:
            read_settings("/definitely/not/here.conf")
        self.assertIn("cannot open", str(ctx.exception))

    def test_bad_line_reports_line_number(self):
        path = self.write("a = 1\n# comment\n\nnonsense\n")
        with self.assertRaises(ConfigError) as ctx:
            read_settings(path)
        self.assertEqual(str(ctx.exception), "line 4: expected key=value")

    def test_unrelated_errors_are_not_swallowed(self):
        with self.assertRaises(TypeError):
            read_settings(None)


if __name__ == "__main__":
    unittest.main()
