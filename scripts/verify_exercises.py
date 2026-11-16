#!/usr/bin/env python3
"""Sanity-check every exercise (for people writing exercises, not learners).

For each exercise this confirms:
  * the reference solution passes the tests and meets every quality goal
  * the starter passes the tests (or fails them, if starter_tests_pass = false)
  * the starter misses at least one quality goal (otherwise there's nothing to do)

Usage: python3 scripts/verify_exercises.py [filter]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from refactor_town.catalog import all_exercises  # noqa: E402
from refactor_town.checks import run_checks  # noqa: E402
from refactor_town.languages import run_tests  # noqa: E402


def main():
    flt = sys.argv[1] if len(sys.argv) > 1 else ""
    problems = 0
    for ex in all_exercises():
        if flt not in ex.id:
            continue
        issues = []
        sol_tests = run_tests(ex, ex.solution_dir)
        if not sol_tests.passed:
            issues.append("solution fails tests:\n" + sol_tests.output[-3000:])
        for r in run_checks(ex, ex.solution_dir):
            if not r.passed:
                issues.append(f"solution misses goal: {r.goal} :: {r.detail}")
        st_tests = run_tests(ex, ex.starter_dir)
        if st_tests.passed != ex.starter_tests_pass:
            want = "pass" if ex.starter_tests_pass else "fail"
            issues.append(f"starter tests should {want}:\n" + st_tests.output[-3000:])
        st_checks = run_checks(ex, ex.starter_dir)
        failing = [r.goal for r in st_checks if not r.passed]
        if not failing:
            issues.append("starter already meets every goal")
        status = "ok " if not issues else "BAD"
        print(f"[{status}] {ex.id}  (starter misses {len(failing)}/{len(st_checks)} goals)")
        for i in issues:
            print("      " + i.replace("\n", "\n      "))
        problems += bool(issues)
    print(f"\n{problems} exercise(s) with problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
