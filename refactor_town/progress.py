"""Remembers which exercise you're on, how many hints you've revealed, and
what you've completed. Stored in workspace/.progress.json."""

import json

from .catalog import WORKSPACE

PATH = WORKSPACE / ".progress.json"


class Progress:
    def __init__(self):
        try:
            self.data = json.loads(PATH.read_text())
        except (OSError, ValueError):
            self.data = {}
        self.data.setdefault("current", None)
        self.data.setdefault("exercises", {})

    def save(self):
        PATH.parent.mkdir(parents=True, exist_ok=True)
        PATH.write_text(json.dumps(self.data, indent=2))

    def _entry(self, ex_id):
        return self.data["exercises"].setdefault(ex_id, {"status": "started", "hints": 0, "checks": 0})

    @property
    def current(self):
        return self.data["current"]

    @current.setter
    def current(self, ex_id):
        self.data["current"] = ex_id
        self._entry(ex_id)
        self.save()

    def status(self, ex_id):
        e = self.data["exercises"].get(ex_id)
        return e["status"] if e else "new"

    def hints_used(self, ex_id):
        return self._entry(ex_id)["hints"]

    def reveal_hint(self, ex_id):
        e = self._entry(ex_id)
        e["hints"] += 1
        self.save()
        return e["hints"]

    def record_check(self, ex_id, solved):
        e = self._entry(ex_id)
        e["checks"] = e.get("checks", 0) + 1
        first_time = solved and e["status"] != "done"
        if solved:
            e["status"] = "done"
            e.setdefault("solved_after_checks", e["checks"])
            e.setdefault("solved_with_hints", e["hints"])
        self.save()
        return first_time

    def mark_peeked(self, ex_id):
        self._entry(ex_id)["peeked"] = True
        self.save()

    def reset(self, ex_id):
        self.data["exercises"].pop(ex_id, None)
        self._entry(ex_id)
        self.save()
