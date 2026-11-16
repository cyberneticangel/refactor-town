"""Per-language knowledge: how to run the behaviour tests, how comments and
functions look (used by the quality checks)."""

import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Language:
    key: str
    name: str
    short: str                # code used in `start py1`, `list` etc.
    aliases: tuple
    tools: tuple              # executables that must be on PATH
    line_comment: str
    block_comments: bool
    function_header: str      # regex that marks the start of a function (brace languages)
    install_hint: str

    def steps(self, build: Path):
        """The commands that compile and run the tests inside `build`."""
        k = self.key
        if k == "python":
            return [[sys.executable, "-m", "unittest", "discover", "-s", ".", "-p", "test_*.py", "-v"]]
        if k == "javascript":
            return [["node", "--test", *sorted(p.name for p in build.glob("*.test.mjs"))]]
        if k == "go":
            return [["go", "test", "-count=1", "-v", "./..."]]
        if k == "rust":
            return [
                ["rustc", "--edition", "2021", "--test", "-A", "dead_code", "harness.rs", "-o", "tests_bin"],
                ["./tests_bin", "--test-threads=1"],
            ]
        if k == "java":
            return [["java", "Tests.java"]]
        if k == "c":
            sources = sorted(p.name for p in build.glob("*.c"))
            return [
                ["gcc", "-std=c11", "-Wall", "-Wextra", "-g", "-O0",
                 "-fsanitize=address,undefined", "-fno-omit-frame-pointer",
                 *sources, "-o", "tests_bin"],
                ["./tests_bin"],
            ]
        raise KeyError(k)

    def env(self):
        env = dict(os.environ)
        if self.key == "go":
            env.setdefault("GOTOOLCHAIN", "local")
            env.setdefault("GOFLAGS", "-mod=mod")
        if self.key == "c":
            env.setdefault("ASAN_OPTIONS", "detect_leaks=1")
        if self.key == "python":
            env["PYTHONDONTWRITEBYTECODE"] = "1"
        return env

    def missing_tools(self):
        return [t for t in self.tools if shutil.which(t) is None]


LANGUAGES = {
    "python": Language(
        "python", "Python", "py", ("py", "python3"), (), "#", False, r"^\s*(async\s+)?def\s",
        "Python 3.11+ is required (you are already running it)."),
    "javascript": Language(
        "javascript", "JavaScript", "js", ("js", "node", "javascript"), ("node",), "//", True,
        r"^\s*(export\s+)?(async\s+)?function\b|^\s*(export\s+)?const\s+\w+\s*=\s*(async\s*)?\([^)]*\)\s*=>\s*\{",
        "Install Node.js 20+ (https://nodejs.org)."),
    "go": Language(
        "go", "Go", "go", ("golang",), ("go",), "//", True, r"^func\b",
        "Install Go 1.22+ (https://go.dev/dl)."),
    "rust": Language(
        "rust", "Rust", "rs", ("rs",), ("rustc",), "//", True,
        r"^\s*(pub(\([\w:]+\))?\s+)?(const\s+)?(async\s+)?fn\s+\w+",
        "Install Rust via rustup (https://rustup.rs)."),
    "java": Language(
        "java", "Java", "java", ("jv",), ("java",), "//", True,
        r"^\s+(?:(?:public|private|protected|static|final|synchronized|abstract|default)\s+)+"
        r"(?:[\w<>\[\],.?]+(?:\s*<[^>]*>)?\s+)?\w+\s*\([^;]*$",
        "Install a JDK 22+ (https://adoptium.net)."),
    "c": Language(
        "c", "C", "c", ("clang", "gcc"), ("gcc",), "//", True,
        r"^(?!typedef|struct\s+\w+\s*\{|enum|#|return)[A-Za-z_][\w\s\*]*\b\w+\s*\([^;]*$",
        "Install gcc with AddressSanitizer support (usually in your distro's gcc package)."),
}


def resolve_language(name):
    name = name.strip().lower()
    if name in LANGUAGES:
        return name
    for key, lang in LANGUAGES.items():
        if name == lang.short:
            return key
    for key, lang in LANGUAGES.items():
        if name in lang.aliases or lang.name.lower() == name:
            return key
    return None


@dataclass
class TestRun:
    passed: bool
    output: str
    missing: list


def run_tests(exercise, source_dir: Path, timeout=120) -> TestRun:
    """Copy the learner's files plus the hidden tests into a fresh build dir
    and run the language's test steps there."""
    lang = LANGUAGES[exercise.language]
    missing = lang.missing_tools()
    if missing:
        return TestRun(False, f"Missing tools: {', '.join(missing)}. {lang.install_hint}", missing)

    build = exercise.build_dir
    if build.exists():
        shutil.rmtree(build)
    build.mkdir(parents=True)
    for src in (source_dir, exercise.tests_dir):  # tests last: they win on name clashes
        for f in src.iterdir():
            if f.is_file():
                shutil.copy2(f, build / f.name)

    out = []
    for step in lang.steps(build):
        try:
            proc = subprocess.run(
                step, cwd=build, env=lang.env(), capture_output=True,
                text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            out.append(f"Timed out after {timeout}s running: {' '.join(step)}\n"
                       "(an infinite loop, perhaps?)")
            return TestRun(False, "".join(out), [])
        out.append(proc.stdout)
        out.append(proc.stderr)
        if proc.returncode != 0:
            return TestRun(False, "".join(out), [])
    return TestRun(True, "".join(out), [])
