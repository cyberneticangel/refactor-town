"""The interactive `town>` prompt, also usable one-shot: ./town check"""

import cmd
import difflib
import os
import re
import shlex
import shutil
import subprocess
import time

from . import ui
from .catalog import all_exercises, find
from .checks import run_checks
from .languages import LANGUAGES, resolve_language, run_tests
from .progress import Progress

BANNER = r"""
  ┌─────────────────────────────────────────────────────────┐
  │   R E F A C T O R   T O W N                             │
  │   learn to program by making working code better        │
  └─────────────────────────────────────────────────────────┘
"""


class Shell(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.exercises = all_exercises()
        self.progress = Progress()
        self._refresh_prompt()

    # -- plumbing ----------------------------------------------------------

    def _refresh_prompt(self):
        cur = self.progress.current
        label = ui.cyan(cur) if cur else ui.gray("no exercise")
        self.prompt = f"{label} {ui.bold('›')} "

    def current(self, quiet=False):
        ex = find(self.progress.current, self.exercises) if self.progress.current else None
        if ex is None and not quiet:
            print(f"  No exercise open. Try {ui.yellow('list')} then {ui.yellow('start py1')}.")
        return ex

    def emptyline(self):
        pass

    def default(self, line):
        print(f"  Unknown command {ui.red(line.split()[0])}. Type {ui.yellow('help')} for the list.")

    def postcmd(self, stop, line):
        self._refresh_prompt()
        return stop

    def do_EOF(self, _):
        print()
        return True

    def do_quit(self, _):
        """Leave Refactor Town (your work is saved in workspace/)."""
        print("  See you next time. Your files stay in workspace/.")
        return True

    do_exit = do_quit
    do_q = do_quit

    def preloop(self):
        print(ui.style(BANNER, "cyan"))
        done = sum(1 for e in self.exercises if self.progress.status(e.id) == "done")
        print(f"  {done}/{len(self.exercises)} exercises completed across {len(LANGUAGES)} languages.")
        ex = self.current(quiet=True)
        if ex:
            print(f"  You're working on {ui.bold(ex.title)} ({ex.id}).")
            print(f"  Edit files in {ui.yellow(self._rel(ex.workspace_dir))}, then type {ui.yellow('check')}.")
        else:
            print(f"  New here? Type {ui.yellow('tour')} for a 1-minute orientation, or {ui.yellow('list')} to browse.")
        print()

    @staticmethod
    def _rel(path):
        try:
            return os.path.relpath(path)
        except ValueError:
            return str(path)

    # -- browsing ----------------------------------------------------------

    def do_tour(self, _):
        """How Refactor Town works."""
        ui.heading("How this works")
        ui.prose("""
        Refactoring means changing the *shape* of code without changing what it *does*.
        Every exercise gives you a small program that works but is hard to read or change.
        Your job: make it better while keeping its behaviour identical.

        1. `start py1` copies the messy code into `workspace/` and shows the brief.
        2. Open those files in any editor you like.
        3. `lesson` teaches the concept the exercise is built around.
        4. `check` runs two things:
           - behaviour tests: your safety net. If they go red, you changed what the code does.
           - quality goals: the specific improvements this exercise asks for.
        5. Stuck? `hint` reveals hints one at a time, from gentle nudges to near-answers.
        6. `watch` re-checks every time you save, which is the best way to work.
        7. When everything is green you'll get a debrief, then `next`.

        Tip: refactor in small steps and check after each one. If the tests break, you know
        exactly which change did it. That habit is the real lesson.
        """)
        print()

    def do_list(self, arg):
        """list [language] - show exercises and your progress."""
        lang = resolve_language(arg) if arg.strip() else None
        if arg.strip() and not lang:
            print(f"  Unknown language {arg!r}. Options: {', '.join(LANGUAGES)}")
            return
        current_lang = None
        for ex in self.exercises:
            if lang and ex.language != lang:
                continue
            if ex.language != current_lang:
                current_lang = ex.language
                info = LANGUAGES[ex.language]
                missing = info.missing_tools()
                tag = ui.red(f"  (needs {', '.join(missing)})") if missing else ""
                ui.heading(f"{info.name}{tag}")
            status = self.progress.status(ex.id)
            mark = {"done": ui.green(ui.OK), "started": ui.yellow(ui.DOT)}.get(status, " ")
            here = ui.cyan(" ◂ current") if ex.id == self.progress.current else ""
            bug = ui.magenta(" [fix]") if not ex.starter_tests_pass else ""
            short = f"{info.short}{ex.number}"
            print(f"   {mark} {ui.gray(short.ljust(6))} {ui.stars(ex.difficulty)}  {ex.title}{bug}{here}")
        print()
        print(ui.gray(f"   {ui.OK} done   {ui.DOT} started   [fix] starts with failing tests: refactor to fix a real bug"))
        print(ui.gray("   Start one with: start py1   (or start rust/3, start go/interfaces …)"))

    def do_progress(self, _):
        """Summary of your progress per language."""
        ui.heading("Progress")
        for key, info in LANGUAGES.items():
            exs = [e for e in self.exercises if e.language == key]
            if not exs:
                continue
            done = sum(self.progress.status(e.id) == "done" for e in exs)
            bar = ui.green("█" * done) + ui.gray("░" * (len(exs) - done))
            print(f"   {info.name.ljust(11)} {bar} {done}/{len(exs)}")
        print()

    # -- starting / navigating -------------------------------------------

    def do_start(self, arg):
        """start <exercise> - open an exercise (e.g. start py1, start rust/2)."""
        if not arg.strip():
            print("  Which one? e.g. start py1. Use list to see them all.")
            return
        ex = find(arg, self.exercises)
        if not ex:
            print(f"  No exercise matches {arg!r}. Try list.")
            return
        self._open(ex)

    do_open = do_start

    def _open(self, ex):
        fresh = not ex.workspace_dir.exists()
        if fresh:
            shutil.copytree(ex.starter_dir, ex.workspace_dir)
        self.progress.current = ex.id
        info = LANGUAGES[ex.language]
        print()
        ui.rule(f"{info.name} · {ex.slug}")
        print(f"  {ui.bold(ex.title)}   {ui.stars(ex.difficulty)}")
        if ex.concepts:
            print(ui.gray(f"  concepts: {', '.join(ex.concepts)}"))
        ui.rule()
        ui.prose(ex.brief)
        print()
        files = ", ".join(ex.files)
        print(f"  {ui.bold('Your files:')} {ui.yellow(self._rel(ex.workspace_dir))}/  ({files})")
        if not fresh:
            print(ui.gray("  (Continuing from where you left off. Use `reset` to start over.)"))
        missing = info.missing_tools()
        if missing:
            print(ui.red(f"  Heads up: {', '.join(missing)} not found. {info.install_hint}"))
        print(f"  Next: {ui.yellow('lesson')} to learn the idea · {ui.yellow('check')} to see where you stand · "
              f"{ui.yellow('watch')} to auto-check on save")
        print()

    def do_next(self, _):
        """Move on to the next unfinished exercise."""
        cur = self.current(quiet=True)
        order = self.exercises
        start = order.index(cur) + 1 if cur else 0
        for ex in order[start:] + order[:start]:
            if self.progress.status(ex.id) != "done":
                self._open(ex)
                return
        print(ui.green("  You've completed every exercise in Refactor Town. Incredible work."))

    def do_brief(self, _):
        """Re-read the current exercise's brief."""
        ex = self.current()
        if ex:
            self._open(ex)

    def do_lesson(self, _):
        """Teach the concept behind the current exercise."""
        ex = self.current()
        if not ex:
            return
        ui.heading(f"Lesson · {ex.title}", "magenta")
        ui.prose(ex.lesson or "This exercise has no separate lesson. The brief and hints carry it.")
        print()

    do_learn = do_lesson
    do_concept = do_lesson

    def do_hint(self, _):
        """Reveal the next hint (they get more specific each time)."""
        ex = self.current()
        if not ex:
            return
        used = self.progress.hints_used(ex.id)
        if used >= len(ex.hints):
            print(f"  That's all {len(ex.hints)} hints. Still stuck? `compare` shows the gap between your code and a "
                  "reference solution, or `solution` shows it outright.")
            self._show_hints(ex, len(ex.hints))
            return
        n = self.progress.reveal_hint(ex.id)
        ui.heading(f"Hint {n}/{len(ex.hints)}", "yellow")
        ui.prose(ex.hints[n - 1])
        if n < len(ex.hints):
            print(ui.gray(f"\n  (`hint` again for a more specific one, `hints` to re-read the ones you have)"))
        print()

    def do_hints(self, _):
        """Show all hints you've revealed so far."""
        ex = self.current()
        if ex:
            self._show_hints(ex, self.progress.hints_used(ex.id))

    def _show_hints(self, ex, n):
        if n == 0:
            print("  No hints revealed yet. Type `hint`.")
        for i in range(n):
            ui.heading(f"Hint {i + 1}/{len(ex.hints)}", "yellow")
            ui.prose(ex.hints[i])
        print()

    # -- checking ------------------------------------------------------------

    def do_check(self, arg, from_watch=False):
        """Run behaviour tests and quality goals on your code."""
        ex = find(arg, self.exercises) if arg.strip() else self.current()
        if not ex:
            return False
        if not ex.workspace_dir.exists():
            self._open(ex)
        print()
        print(ui.bold("  Behaviour") + ui.gray("  (does it still do the same thing?)"))
        t0 = time.time()
        result = run_tests(ex, ex.workspace_dir)
        took = time.time() - t0
        if result.passed:
            print(f"   {ui.green(ui.OK)} all tests pass {ui.gray(f'({took:.1f}s)')}")
        else:
            print(f"   {ui.red(ui.FAIL)} tests failing {ui.gray(f'({took:.1f}s)')}")
            self._show_failure(result.output)

        print()
        print(ui.bold("  Quality goals") + ui.gray("  (is it better?)"))
        results = run_checks(ex, ex.workspace_dir)
        for r in results:
            if r.passed:
                print(f"   {ui.green(ui.OK)} {r.goal}")
            else:
                print(f"   {ui.red(ui.FAIL)} {r.goal}")
                if r.detail:
                    ui.prose(ui.gray(r.detail), indent="       ")
        met = sum(r.passed for r in results)
        solved = result.passed and met == len(results)
        first = self.progress.record_check(ex.id, solved)

        print()
        if solved:
            ui.rule()
            print(ui.green(ui.bold(f"  {ui.OK} Solved! Behaviour preserved and all {len(results)} goals met.")))
            if first and ex.debrief:
                ui.heading("Debrief", "green")
                ui.prose(ex.debrief)
                print()
            print(f"  Compare with a reference refactoring: {ui.yellow('solution')}   ·   Move on: {ui.yellow('next')}")
            ui.rule()
        else:
            bar = ui.green("■" * met) + ui.gray("□" * (len(results) - met))
            print(f"  {bar}  {met}/{len(results)} goals" + ("" if result.passed else ui.red("  · tests failing")))
            if not result.passed and met == len(results):
                print(ui.yellow("  The code looks better, but behaviour changed. Undo your last step and try a smaller one."))
            elif not from_watch and self.progress.hints_used(ex.id) < len(ex.hints):
                print(ui.gray("  Need a nudge? Type `hint`."))
        print()
        return solved

    @staticmethod
    def _show_failure(output, max_lines=40):
        """Show the most useful part of a failed run: lines that name a failure
        first (they're often buried above long sanitizer/compiler output),
        then the tail of the log."""
        lines = [l for l in output.rstrip().splitlines() if l.strip()]
        if not lines:
            return
        if len(lines) <= max_lines:
            shown = lines
        else:
            key = re.compile(r"FAIL|AssertionError|panicked|error[:\[]|ERROR|Error:|not ok|leaked|expected")
            important = [i for i, l in enumerate(lines) if key.search(l)][:12]
            tail_start = len(lines) - (max_lines - len(important))
            picked = sorted(set(important) | set(range(max(tail_start, 0), len(lines))))
            shown, prev = [], None
            for i in picked:
                if prev is not None and i != prev + 1:
                    shown.append(ui.gray("…"))
                shown.append(lines[i])
                prev = i
            print(ui.gray(f"     (showing the key {len(picked)} of {len(lines)} lines; `testlog` shows everything)"))
        for line in shown:
            print("     " + ui.gray("│ ") + line)

    def do_testlog(self, _):
        """Show the full output of the last test run."""
        ex = self.current()
        if not ex:
            return
        run = run_tests(ex, ex.workspace_dir)
        print(run.output)

    def do_watch(self, arg):
        """Re-run `check` automatically whenever you save a file (Ctrl-C to stop)."""
        ex = self.current()
        if not ex:
            return

        def snapshot():
            return {p: p.stat().st_mtime for p in ex.workspace_dir.rglob("*") if p.is_file()}

        last = None
        try:
            while True:
                snap = snapshot()
                if snap != last:
                    last = snap
                    ui.clear()
                    ui.rule(f"watching {ex.id} · Ctrl-C to stop")
                    self.do_check("", from_watch=True)
                    print(ui.gray(f"  Waiting for you to save a file in {self._rel(ex.workspace_dir)} …"))
                time.sleep(0.6)
        except KeyboardInterrupt:
            print("\n  Stopped watching.")

    # -- looking at code -----------------------------------------------------

    def do_diff(self, _):
        """Show what you've changed compared with the original messy code."""
        ex = self.current()
        if ex:
            self._diff(ex.starter_dir, ex.workspace_dir, ex.files, "original", "yours")

    def do_compare(self, _):
        """Diff your code against the reference solution (a spoiler, but a gentle one)."""
        ex = self.current()
        if not ex:
            return
        if not self._confirm_spoiler(ex):
            return
        self._diff(ex.workspace_dir, ex.solution_dir, ex.files, "yours", "reference")

    def _diff(self, a_dir, b_dir, files, a_label, b_label):
        any_change = False
        for name in files:
            a = (a_dir / name).read_text().splitlines() if (a_dir / name).exists() else []
            b = (b_dir / name).read_text().splitlines() if (b_dir / name).exists() else []
            diff = list(difflib.unified_diff(a, b, f"{a_label}/{name}", f"{b_label}/{name}", lineterm=""))
            for line in diff:
                any_change = True
                if line.startswith(("+++", "---")):
                    print(ui.bold(line))
                elif line.startswith("+"):
                    print(ui.green(line))
                elif line.startswith("-"):
                    print(ui.red(line))
                elif line.startswith("@@"):
                    print(ui.cyan(line))
                else:
                    print(line)
        if not any_change:
            print("  No differences.")

    def do_tests(self, _):
        """Print the behaviour tests (reading them shows what must not change)."""
        ex = self.current()
        if not ex:
            return
        for f in sorted(ex.tests_dir.iterdir()):
            if f.is_file() and f.name != "go.mod":
                ui.rule(f.name)
                print(f.read_text())

    def do_solution(self, _):
        """Show a reference refactoring (asks first if you haven't solved it)."""
        ex = self.current()
        if not ex or not self._confirm_spoiler(ex):
            return
        for name in ex.files:
            p = ex.solution_dir / name
            if p.exists():
                ui.rule(f"reference · {name}")
                print(p.read_text())
        print(ui.gray("  This is *a* good answer, not *the* answer. If yours differs but passes, compare the trade-offs."))

    def _confirm_spoiler(self, ex):
        if self.progress.status(ex.id) == "done":
            return True
        try:
            ans = input(f"  You haven't solved this yet. Peek anyway? [y/N] ").strip().lower()
        except EOFError:
            ans = ""
        if ans in ("y", "yes"):
            self.progress.mark_peeked(ex.id)
            return True
        print("  Good call. Try `hint` first.")
        return False

    def do_reset(self, _):
        """Throw away your changes and restore the original messy code."""
        ex = self.current()
        if not ex:
            return
        try:
            ans = input(f"  Reset {ex.id}? Your edits will be lost. [y/N] ").strip().lower()
        except EOFError:
            ans = ""
        if ans not in ("y", "yes"):
            print("  Kept your work.")
            return
        shutil.rmtree(ex.workspace_dir, ignore_errors=True)
        shutil.copytree(ex.starter_dir, ex.workspace_dir)
        self.progress.reset(ex.id)
        print(f"  Restored the original code in {self._rel(ex.workspace_dir)}.")

    def do_path(self, _):
        """Print the folder holding your files for this exercise."""
        ex = self.current()
        if ex:
            print(ex.workspace_dir)

    def do_edit(self, arg):
        """edit [file] - open your file(s) in $VISUAL / $EDITOR."""
        ex = self.current()
        if not ex:
            return
        editor = os.environ.get("VISUAL") or os.environ.get("EDITOR")
        if not editor:
            print(f"  Set $EDITOR (e.g. export EDITOR=nvim), or open {ex.workspace_dir} in any editor.")
            return
        targets = [arg.strip()] if arg.strip() else ex.files
        subprocess.call([*shlex.split(editor), *[str(ex.workspace_dir / t) for t in targets]])

    # -- help --------------------------------------------------------------

    def do_help(self, arg):
        if arg:
            return super().do_help(arg)
        groups = [
            ("Getting around", ["tour", "list", "progress", "start", "next", "brief"]),
            ("Learning", ["lesson", "hint", "hints", "tests"]),
            ("Working", ["check", "watch", "diff", "edit", "path", "testlog"]),
            ("Spoilers & do-overs", ["compare", "solution", "reset"]),
            ("", ["quit"]),
        ]
        for title, names in groups:
            if title:
                ui.heading(title)
            for n in names:
                doc = (getattr(self, f"do_{n}").__doc__ or "").strip().splitlines()[0]
                if " - " in doc and doc.split(" - ")[0].startswith(n):
                    usage, doc = doc.split(" - ", 1)
                else:
                    usage = n
                print(f"   {ui.yellow(usage.ljust(20))} {doc}")
        print()
