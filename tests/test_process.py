#!/usr/bin/env python3
import csv
import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import process


class FakeCompletions:
    def __init__(self, captured):
        self.captured = captured

    def create(self, **kwargs):
        self.captured["request"] = kwargs
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(
            content="### **TRIGGER_SUMMARY**: **Work fear**\n\n## Thesis\nA hard day."
        ))])


class FakeOpenAI:
    def __init__(self, captured, **kwargs):
        captured["client"] = kwargs
        self.chat = SimpleNamespace(completions=FakeCompletions(captured))


class ProcessTests(unittest.TestCase):
    def test_seeds_prompt_uses_configured_base_url_and_parses_markdown_summary(self):
        captured = {}

        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir) / "shadow_mirror"
            raw_dir = config_dir / "raw"
            raw_dir.mkdir(parents=True)
            timestamp = "20260711_150000"
            (raw_dir / f"entry_{timestamp}.txt").write_text("I am worried about work.")

            old_env = os.environ.copy()
            old_argv = sys.argv
            old_client = process.OpenAI
            try:
                os.environ["XDG_CONFIG_HOME"] = temp_dir
                os.environ["OPENROUTER_API_KEY"] = "test"
                os.environ["OPENROUTER_BASE_URL"] = "http://localhost:11434/v1"
                process.OpenAI = lambda **kwargs: FakeOpenAI(captured, **kwargs)
                sys.argv = ["process.py", timestamp, "Yellow"]
                process.main()
            finally:
                process.OpenAI = old_client
                sys.argv = old_argv
                os.environ.clear()
                os.environ.update(old_env)

            self.assertEqual(captured["client"]["base_url"], "http://localhost:11434/v1")
            self.assertTrue((config_dir / "prompt.md").exists())
            with (config_dir / "data" / "entries.csv").open(newline="") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(rows[-1]["trigger_summary"], "Work fear")

    def test_patterns_sends_trigger_history_to_the_model(self):
        captured = {}

        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir) / "shadow_mirror"
            data_dir = config_dir / "data"
            data_dir.mkdir(parents=True)
            with (data_dir / "entries.csv").open("w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "spoons", "trigger_summary"])
                writer.writerow(["20260701_090000", "Yellow", "work replacement fear"])
                writer.writerow(["20260702_090000", "Green", "work replacement fear"])

            old_env = os.environ.copy()
            old_client = process.OpenAI
            try:
                os.environ["XDG_CONFIG_HOME"] = temp_dir
                os.environ["OPENROUTER_API_KEY"] = "test"
                process.OpenAI = lambda **kwargs: FakeOpenAI(captured, **kwargs)
                self.assertEqual(process.show_patterns(), 0)
            finally:
                process.OpenAI = old_client
                os.environ.clear()
                os.environ.update(old_env)

            prompt = captured["request"]["messages"][1]["content"]
            self.assertIn("work replacement fear", prompt)

    def test_patterns_without_history_returns_a_calm_message(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            old_env = os.environ.copy()
            try:
                os.environ["XDG_CONFIG_HOME"] = temp_dir
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(process.show_patterns(), 0)
            finally:
                os.environ.clear()
                os.environ.update(old_env)

            self.assertEqual(output.getvalue().strip(), "No trigger history yet.")


if __name__ == "__main__":
    unittest.main()
