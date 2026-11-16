"""Discovering and loading exercises from the exercises/ tree.

Layout of one exercise:

    exercises/<language>/<NN-slug>/
        exercise.toml   metadata, lesson, hints, quality checks
        starter/        the messy code the learner copies into workspace/
        tests/          behaviour tests (hidden harness, copied in at test time)
        solution/       one possible refactoring
"""

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXERCISES = ROOT / "exercises"
WORKSPACE = ROOT / "workspace"
BUILD = ROOT / ".build"


@dataclass
class Exercise:
    id: str                 # "python/01-names"
    language: str           # "python"
    slug: str               # "01-names"
    number: int
    path: Path
    title: str
    difficulty: int
    files: list             # learner-editable files the checks look at
    concepts: list
    brief: str
    lesson: str
    debrief: str
    hints: list
    checks: list
    starter_tests_pass: bool = True
    extra: dict = field(default_factory=dict)

    @property
    def starter_dir(self): return self.path / "starter"

    @property
    def tests_dir(self): return self.path / "tests"

    @property
    def solution_dir(self): return self.path / "solution"

    @property
    def workspace_dir(self): return WORKSPACE / self.language / self.slug

    @property
    def build_dir(self): return BUILD / self.language / self.slug


def _load(path: Path) -> Exercise:
    data = tomllib.loads((path / "exercise.toml").read_text())
    language = path.parent.name
    slug = path.name
    return Exercise(
        id=f"{language}/{slug}",
        language=language,
        slug=slug,
        number=int(slug.split("-", 1)[0]),
        path=path,
        title=data["title"],
        difficulty=data.get("difficulty", 1),
        files=data["files"],
        concepts=data.get("concepts", []),
        brief=data["brief"],
        lesson=data.get("lesson", ""),
        debrief=data.get("debrief", ""),
        hints=data.get("hints", []),
        checks=data.get("checks", []),
        starter_tests_pass=data.get("starter_tests_pass", True),
    )


def all_exercises():
    from .languages import LANGUAGES
    found = []
    for lang in LANGUAGES:  # keeps a stable, curated language order
        d = EXERCISES / lang
        if not d.is_dir():
            continue
        for ex in sorted(p for p in d.iterdir() if (p / "exercise.toml").exists()):
            found.append(_load(ex))
    return found


def find(ref: str, exercises=None):
    """Resolve loose references: 'python/01-names', 'python/1', 'py1', 'py/names'."""
    from .languages import resolve_language
    exercises = exercises or all_exercises()
    ref = ref.strip().lower()

    for ex in exercises:
        if ex.id == ref:
            return ex

    lang_part, _, rest = ref.partition("/")
    if not rest:  # forms like "py1", "rust3"
        head = lang_part.rstrip("0123456789")
        rest = lang_part[len(head):]
        lang_part = head
    lang = resolve_language(lang_part)
    if not lang or not rest:
        return None
    candidates = [e for e in exercises if e.language == lang]
    if rest.isdigit():
        for e in candidates:
            if e.number == int(rest):
                return e
    for e in candidates:
        if rest in e.slug:
            return e
    return None
