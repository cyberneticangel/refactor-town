"""Terminal presentation helpers: colors, boxes, wrapped text."""

import os
import re
import shutil
import sys
import textwrap

_COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ

_CODES = {
    "bold": "1", "dim": "2", "italic": "3", "under": "4",
    "red": "31", "green": "32", "yellow": "33", "blue": "34",
    "magenta": "35", "cyan": "36", "gray": "90",
}


def style(text, *names):
    if not _COLOR or not names:
        return text
    codes = ";".join(_CODES[n] for n in names)
    return f"\033[{codes}m{text}\033[0m"


def bold(t): return style(t, "bold")
def dim(t): return style(t, "dim")
def red(t): return style(t, "red")
def green(t): return style(t, "green")
def yellow(t): return style(t, "yellow")
def cyan(t): return style(t, "cyan")
def magenta(t): return style(t, "magenta")
def gray(t): return style(t, "gray")


OK = "✓"
FAIL = "✗"
DOT = "•"


def width():
    return min(shutil.get_terminal_size((88, 24)).columns, 100)


def rule(title=""):
    w = width()
    if title:
        title = f" {title} "
        print(style("──" + title + "─" * max(0, w - len(title) - 2), "gray"))
    else:
        print(style("─" * w, "gray"))


def heading(text, color="cyan"):
    print()
    print(style(text, "bold", color))


def prose(text, indent="  "):
    """Print authored text: paragraphs and bullets are re-wrapped to the
    terminal, code (```fences``` or 4-space-indented lines) is left alone,
    `code` and **bold** spans are highlighted."""
    w = width() - len(indent)
    in_fence = False
    block = []          # lines of the paragraph/bullet being collected
    bullet = None       # the bullet's hanging indent, or None for a paragraph

    def flush():
        nonlocal bullet
        if block:
            joined = " ".join(s.strip() for s in block)
            hang = bullet or ""
            first = (" " * (len(hang) - 2)) if bullet else ""
            for line in textwrap.wrap(joined, w, initial_indent=first, subsequent_indent=hang) or [""]:
                print(indent + _inline(line))
            block.clear()
        bullet = None

    for raw in textwrap.dedent(text).strip("\n").splitlines():
        stripped = raw.strip()
        if stripped.startswith("```"):
            flush()
            in_fence = not in_fence
            continue
        if in_fence or raw.startswith("    "):
            flush()
            print(indent + style(raw, "yellow"))
        elif not stripped:
            flush()
            print()
        elif re.match(r"\s*([-*]|\d+\.)\s", raw):
            flush()
            lead = len(raw) - len(raw.lstrip())
            marker = re.match(r"\s*([-*]|\d+\.)\s", raw).group(0)
            bullet = " " * (lead + len(marker.strip()) + 3)
            block.append(raw)
        elif bullet is not None and raw[:1] == " ":
            block.append(raw)       # continuation of a wrapped bullet
        else:
            if bullet is not None:
                flush()
            block.append(raw)
    flush()


_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")


def _inline(line):
    """Highlight `code` and **bold** spans (and drop the markers)."""
    line = _BOLD.sub(lambda m: style(m.group(1), "bold"), line)
    return _CODE.sub(lambda m: style(m.group(1), "yellow") if _COLOR else m.group(1), line)


def stars(n, total=3):
    return style("★" * n, "yellow") + style("☆" * (total - n), "gray")


def clear():
    if sys.stdout.isatty():
        print("\033[2J\033[H", end="")
