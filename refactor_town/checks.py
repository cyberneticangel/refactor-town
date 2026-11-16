"""Static "code quality" goals declared in each exercise.toml.

Supported check types (all take `goal` and `message`, optional `file`):

    forbid               regex `pattern` must not appear
    require              regex `pattern` must appear at least `min` times (default 1)
    max_count            regex `pattern` may appear at most `max` times
    max_depth            block nesting may not exceed `max`
                         (Python: indentation blocks; others: brace depth)
    max_function_lines   no function may be longer than `max` lines

Patterns are matched with re.MULTILINE against the source with comments
removed, so explaining your code in a comment never trips a check.
"""

import ast
import io
import re
import tokenize
from dataclasses import dataclass

from .languages import LANGUAGES


@dataclass
class CheckResult:
    goal: str
    passed: bool
    detail: str = ""


# --- source preprocessing ---------------------------------------------------

_STRINGS = re.compile(r'"(?:\\.|[^"\\\n])*"|`(?:\\.|[^`\\])*`|\'(?:\\.|[^\'\\\n])\'', re.S)


def strip_comments(src, lang_key):
    if lang_key == "python":
        return _strip_python_comments(src)
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c in "\"`":
            m = _STRINGS.match(src, i)
            if m:
                out.append(m.group(0))
                i = m.end()
                continue
        if src.startswith("//", i):
            j = src.find("\n", i)
            i = n if j == -1 else j
            continue
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            chunk = src[i:(n if j == -1 else j + 2)]
            out.append("\n" * chunk.count("\n"))  # keep line numbers stable
            i = n if j == -1 else j + 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _strip_python_comments(src):
    lines = src.splitlines(keepends=True)
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, SyntaxError, IndentationError):
        return src
    for tok in reversed(toks):
        if tok.type == tokenize.COMMENT:
            row, col = tok.start
            line = lines[row - 1]
            lines[row - 1] = line[:col].rstrip() + ("\n" if line.endswith("\n") else "")
    return "".join(lines)


def blank_strings(src):
    """Replace string literal contents so braces inside strings don't count."""
    return _STRINGS.sub(lambda m: m.group(0)[0] + " " * (len(m.group(0)) - 2) + m.group(0)[-1], src)


# --- measurements -------------------------------------------------------------

def python_depth(src):
    depth = deepest = 0
    deepest_line = 0
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type == tokenize.INDENT:
                depth += 1
                if depth > deepest:
                    deepest, deepest_line = depth, tok.start[0]
            elif tok.type == tokenize.DEDENT:
                depth -= 1
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass
    return deepest, deepest_line


def brace_depth(src):
    depth = deepest = 0
    deepest_line = 0
    for lineno, line in enumerate(blank_strings(src).splitlines(), 1):
        for ch in line:
            if ch == "{":
                depth += 1
                if depth > deepest:
                    deepest, deepest_line = depth, lineno
            elif ch == "}":
                depth -= 1
    return deepest, deepest_line


def python_functions(src):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []
    out = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            start = min([node.lineno] + [d.lineno for d in node.decorator_list])
            out.append((node.name, node.lineno, node.end_lineno - start + 1))
    return out


_KEYWORDS = {"func", "fn", "function", "if", "for", "while", "switch", "return", "new", "catch", "sizeof"}


def brace_functions(src, header_regex):
    header = re.compile(header_regex)
    lines = blank_strings(src).splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if header.search(line) and not re.match(r"\s*(if|for|while|switch|catch|return|else)\b", line):
            names = [n for n in re.findall(r"(\w+)\s*(?:<[^>]*>)?\s*\(", line) if n not in _KEYWORDS]
            name = names[0] if names else "?"
            depth, opened, j = 0, False, i
            while j < len(lines):
                for ch in lines[j]:
                    if ch == "{":
                        depth += 1
                        opened = True
                    elif ch == "}":
                        depth -= 1
                if opened and depth <= 0:
                    break
                if not opened and lines[j].rstrip().endswith(";"):
                    break  # a declaration/prototype, not a definition
                j += 1
            if opened:
                out.append((name, i + 1, j - i + 1))
                i = j + 1
                continue
        i += 1
    return out


# --- running checks -----------------------------------------------------------

def run_checks(exercise, source_dir):
    lang = LANGUAGES[exercise.language]
    sources = {}
    for name in exercise.files:
        p = source_dir / name
        sources[name] = p.read_text() if p.exists() else ""
    stripped = {k: strip_comments(v, lang.key) for k, v in sources.items()}

    results = []
    for chk in exercise.checks:
        targets = [chk["file"]] if "file" in chk else list(stripped)
        results.append(_run_one(chk, {t: stripped.get(t, "") for t in targets}, lang))
    return results


def _run_one(chk, files, lang):
    kind = chk["type"]
    goal = chk["goal"]
    message = chk.get("message", "")
    flags = re.MULTILINE | (re.IGNORECASE if chk.get("ignore_case") else 0)

    if kind in ("forbid", "require", "max_count"):
        rx = re.compile(chk["pattern"], flags)
        hits = []
        for fname, src in files.items():
            for m in rx.finditer(src):
                line = src.count("\n", 0, m.start()) + 1
                hits.append((fname, line, m.group(0).strip()))
        if kind == "forbid":
            ok = not hits
            where = _where(hits)
            return CheckResult(goal, ok, "" if ok else f"{message} {where}".strip())
        if kind == "require":
            need = chk.get("min", 1)
            ok = len(hits) >= need
            return CheckResult(goal, ok, "" if ok else message)
        allowed = chk["max"]
        ok = len(hits) <= allowed
        return CheckResult(goal, ok, "" if ok else f"{message} (found {len(hits)}, allowed {allowed}) {_where(hits)}".strip())

    if kind == "max_depth":
        allowed = chk["max"]
        worst = (0, 0, "")
        for fname, src in files.items():
            d, line = python_depth(src) if lang.key == "python" else brace_depth(src)
            if d > worst[0]:
                worst = (d, line, fname)
        ok = worst[0] <= allowed
        return CheckResult(goal, ok, "" if ok else
                           f"{message} (deepest nesting is {worst[0]} levels at {worst[2]}:{worst[1]}, aim for ≤ {allowed})".strip())

    if kind == "max_function_lines":
        allowed = chk["max"]
        offenders = []
        for fname, src in files.items():
            funcs = python_functions(src) if lang.key == "python" else brace_functions(src, lang.function_header)
            offenders += [(fname, name, line, n) for name, line, n in funcs if n > allowed]
        ok = not offenders
        listed = ", ".join(f"{n}() is {length} lines ({f}:{line})" for f, n, line, length in offenders[:3])
        return CheckResult(goal, ok, "" if ok else f"{message} {listed}; aim for ≤ {allowed}".strip())

    raise ValueError(f"unknown check type {kind!r}")


def _where(hits, limit=3):
    if not hits:
        return ""
    shown = ", ".join(f"{f}:{line} `{text[:40]}`" for f, line, text in hits[:limit])
    more = f" and {len(hits) - limit} more" if len(hits) > limit else ""
    return f"[{shown}{more}]"
