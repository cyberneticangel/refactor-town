import sys

from .shell import Shell


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    shell = Shell()
    if argv:  # one-shot mode: ./town check, ./town start py1, ...
        shell.onecmd(" ".join(argv))
        return 0
    try:
        shell.cmdloop()
    except KeyboardInterrupt:
        print("\n  Bye! Your work is saved in workspace/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
