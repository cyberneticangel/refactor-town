# Refactor Town

**Learn to program by making working code better.**

Most tutorials ask you to write code from a blank page. Refactor Town hands you code that
already *works* but is hard to read, hard to change, or quietly broken, and asks you to
improve it without changing what it does. Along the way you pick up each language's core ideas
the way professionals do: by reading real code, spotting what's wrong with it, and fixing it
safely.

```
$ ./town

  ┌─────────────────────────────────────────────────────────┐
  │   R E F A C T O R   T O W N                             │
  │   learn to program by making working code better        │
  └─────────────────────────────────────────────────────────┘

no exercise › start py1
no exercise › hint
python/01-names › check

  Behaviour  (does it still do the same thing?)
   ✓ all tests pass (0.1s)

  Quality goals  (is it better?)
   ✓ No single-letter variable names
   ✓ The parameter has a descriptive name
   ✗ Loop over items, not over index numbers
       range(len(...)) loops over indexes; loop over the items directly: [stats.py:3 ...]
   ✓ Use the built-in sum()
   ✗ Use the built-in max()

  ■■■□□  3/5 goals
```

---

## Quick start

```sh
./town          # interactive mode (recommended)
```

Then:

1. `tour`: a one-minute orientation
2. `list`: browse all 25 exercises
3. `start py1`: copy the first exercise into `workspace/` and read its brief
4. Open the file it names in **any editor you like**
5. `watch`: re-checks every time you save. Keep it running in a second terminal.

Every command also works one-shot from your shell: `./town check`, `./town hint`, `./town start rs2`.

### Requirements

Only **Python 3.11+** is needed to run Refactor Town itself (no packages to install). Each
language track needs its own toolchain, and `list` flags any that are missing:

| Track      | Needs                                   | Tests run with                          |
|------------|-----------------------------------------|-----------------------------------------|
| Python     | Python 3.11+                            | `unittest`                              |
| JavaScript | Node.js 20+                             | `node --test`                           |
| Go         | Go 1.23+                                | `go test`                               |
| Rust       | `rustc` (via rustup)                    | `rustc --test` (no Cargo needed)        |
| Java       | JDK 22+                                 | the multi-file source launcher          |
| C          | `gcc` with AddressSanitizer             | gcc with `-fsanitize=address,undefined` |

---

## How it works

Each exercise checks your code in two ways:

**Behaviour tests (your safety net).** Hidden tests pin down exactly what the code does. If
they go red, you changed behaviour, not just structure. Undo the last step and take a smaller
one. That habit (small step → check → repeat) is the real skill being taught. `tests` prints
them, and reading them is encouraged.

**Quality goals (what "better" means here).** Each exercise lists specific, checkable
improvements: "no index-based loops", "every function ≤ 12 lines", "the tax rate is written
once", "no `instanceof`". Failed goals point at the exact file and line.

When both are green you get a **debrief** explaining why the change matters and how the same
idea shows up in other languages.

### Hints that escalate

`hint` reveals hints one at a time, from a gentle nudge ("start with the names") down to
near-code ("`valid = [r for r in readings if r >= 0]`"). Use as many as you need; `hints`
re-reads the ones you've unlocked.

### Exercises marked `[fix]`

Some starters come with **failing tests**, because the messy style hides a real bug: a
mutation that breaks undo, a memory leak, a buffer overflow. You refactor *to* fix it. In the
C track, AddressSanitizer and LeakSanitizer show you exactly where things go wrong.

---

## The curriculum

Within each track exercises build on each other (★ easy → ★★★ harder). Across tracks the same
big ideas come back in different syntax, so doing the same idea in a second language is where
it really sticks.

### Python
| # | Exercise | You'll learn |
|---|----------|--------------|
| `py1` | Names that explain themselves | variables, naming, `for` loops, `sum`/`max` |
| `py2` | Untangle nested ifs | guard clauses, `elif`, constants, dict lookup tables |
| `py3` | Don't repeat yourself | functions, parameters, f-string formatting, DRY |
| `py4` | Parallel lists → objects | classes, `@dataclass`, dictionaries, comprehensions |
| `py5` | Exceptions and resources done right | `try`/`except`, `with`, `raise … from`, `enumerate` |

### JavaScript
| # | Exercise | You'll learn |
|---|----------|--------------|
| `js1` | From var-loops to map, filter, reduce | `const`/`let`, `===`, arrow functions, array methods |
| `js2` | Escape callback hell with async/await | callbacks, promises, `async`/`await`, `Promise.all` |
| `js3` | Replace switch with a lookup of behaviours | functions as values, dispatch tables, polymorphism |
| `js4` | Stop mutating state `[fix]` | references, pure functions, spread, immutable updates |

### Go
| # | Exercise | You'll learn |
|---|----------|--------------|
| `go1` | Errors, early returns and the happy path | error values, early return, `%w` wrapping |
| `go2` | One giant function → a type with methods | structs, methods, pointer receivers, `strings.Builder` |
| `go3` | Type switches → interfaces | interfaces, implicit implementation, constructors |
| `go4` | Write it like a Gopher | `range`, maps, `slices.SortFunc`, closures, the stdlib |

### Rust
| # | Exercise | You'll learn |
|---|----------|--------------|
| `rs1` | Index loops → iterators, owned → borrowed | iterators, closures, `&[T]`/`&str`, borrowing |
| `rs2` | Stringly errors → Result, enums and `?` | `Result`, the `?` operator, error enums, `Display` |
| `rs3` | Stringly-typed state → enums and match | enums, exhaustive `match`, `Option` |
| `rs4` | Copy-pasted impls → a trait | traits, default methods, `dyn` trait objects |

### Java
| # | Exercise | You'll learn |
|---|----------|--------------|
| `java1` | Extract method & name the magic numbers | methods, `static final`, single source of truth |
| `java2` | `instanceof` chains → polymorphism | interfaces, records, default methods, dispatch |
| `java3` | Loops → streams, POJOs → records | streams, lambdas, method refs, `Collectors` |
| `java4` | null checks → Optional | `Optional`, `map`/`flatMap`/`orElse` |

### C
| # | Exercise | You'll learn |
|---|----------|--------------|
| `c1` | If-ladders → a lookup table of structs | structs, `static const` arrays, `const`, `size_t` |
| `c2` | Parallel arrays → an array of structs | `->`, enums, `bool`, safe string copies |
| `c3` | Who frees this? `[fix]` | `malloc`/`free`, ownership, leaks, `goto cleanup` |
| `c4` | Buffer overflows → bounded writes `[fix]` | `snprintf`, variadic functions, encapsulation in C |

**Suggested paths**

- *Brand new to programming:* Python start to finish, then JavaScript.
- *Know one language:* do its track quickly, then pick a language that's different from it
  (Python → Rust, JavaScript → Go, Java → C).
- *Want to see one idea everywhere:* "replace conditionals with polymorphism" appears as
  `js3` → `go3` → `rs4` → `java2`. Error handling: `py5` → `go1` → `rs2` → `java4` → `c3`.

---

## Command reference

| Command | What it does |
|---------|--------------|
| `tour` | How Refactor Town works |
| `list [language]` | All exercises with your progress (`✓` done, `•` started) |
| `progress` | Completion per language |
| `start <ref>` | Open an exercise: `py1`, `rust/3`, `go/interfaces`, `java/02-polymorphism` |
| `next` | Jump to the next unfinished exercise |
| `brief` | Re-read the task |
| `lesson` | Teach the concept behind the exercise |
| `hint` / `hints` | Reveal the next hint / re-read revealed hints |
| `tests` | Print the behaviour tests |
| `check` | Run tests + quality goals |
| `watch` | Re-check on every save (Ctrl-C to stop) |
| `diff` | What you've changed vs. the original |
| `edit [file]` | Open your files in `$VISUAL` / `$EDITOR` |
| `path` | Print your workspace folder for this exercise |
| `testlog` | Full, untrimmed test output |
| `compare` | Diff your code against the reference solution *(spoiler)* |
| `solution` | Show a reference refactoring *(asks first if unsolved)* |
| `reset` | Restore the original messy code |
| `quit` | Leave (all progress is saved) |

Your code lives in `workspace/<language>/<exercise>/` and progress in
`workspace/.progress.json`. Delete `workspace/` to start completely fresh.

---

## Project layout

```
refactor-town/
├── town                     launcher script
├── refactor_town/           the CLI (standard library only)
│   ├── shell.py             interactive commands
│   ├── catalog.py           finds and loads exercises
│   ├── languages.py         how to run each language's tests
│   ├── checks.py            the quality-goal engine
│   ├── progress.py          saves your progress
│   └── ui.py                terminal rendering
├── exercises/<language>/<NN-slug>/
│   ├── exercise.toml        brief, lesson, hints, debrief, quality goals
│   ├── starter/             the messy code you start from
│   ├── tests/               hidden behaviour tests
│   └── solution/            one good refactoring
├── scripts/verify_exercises.py
└── workspace/               your work (created on first `start`, git-ignored)
```

---

## Writing your own exercises

An exercise is a folder; nothing needs registering. Copy an existing one in the same language
and edit it. `exercise.toml` looks like this:

```toml
title = "Names that explain themselves"
difficulty = 1                     # 1–3 stars
files = ["stats.py"]               # files the learner edits (and the goals inspect)
concepts = ["naming", "for loops"]
starter_tests_pass = true          # false for [fix] exercises

brief = """What the code does and what to change."""
lesson = """The concept, with small examples."""
debrief = """Shown once, on first solve: why it mattered."""
hints = ["gentle nudge", "more specific", "nearly the answer"]

[[checks]]
type = "forbid"                    # forbid | require | max_count | max_depth | max_function_lines
pattern = 'range\(\s*len\('        # regex, matched with comments stripped
goal = "Loop over items, not over index numbers"
message = "Shown (with file:line) when the goal fails."
```

| Check | Passes when |
|-------|-------------|
| `forbid` | `pattern` never matches |
| `require` | `pattern` matches at least `min` times (default 1) |
| `max_count` | `pattern` matches at most `max` times |
| `max_depth` | nesting ≤ `max` (Python: indented blocks; others: brace depth) |
| `max_function_lines` | every function is ≤ `max` lines |

Any check can take `file = "x.c"` to target one file. Comments are stripped before matching,
so learners can annotate their code freely.

**Test conventions per language:** Python `test_*.py` (unittest) · JavaScript `*.test.mjs`
(node:test) · Go `*_test.go` + `go.mod` · Rust `harness.rs` that declares `mod <file>;` ·
Java `Tests.java` with a `main` that exits non-zero on failure · C `test_*.c` with a `main`
that returns non-zero on failure. Files in `tests/` are copied in *after* the learner's, so a
provided support file (like `api.mjs` in `js2`) can't be tampered with.

Then validate everything:

```sh
python3 scripts/verify_exercises.py          # all exercises
python3 scripts/verify_exercises.py rust/    # filter
```

It confirms the solution passes the tests and every goal, the starter's tests pass (or fail,
for `[fix]` exercises), and the starter misses at least one goal. If any of those fail, the
exercise has a problem.

---

## Philosophy

- **Behaviour is sacred.** Refactoring changes structure, never results. The tests enforce it.
- **Small steps.** Check after every change, so a failure always points at one edit.
- **"Better" is specific.** Each goal names a concrete smell, so you learn to *see* them.
- **One idea, many languages.** Concepts repeat across tracks on purpose.
- **There's no single right answer.** The reference solution is *a* good answer. If yours passes
  and differs, compare the trade-offs. That comparison is learning too.
