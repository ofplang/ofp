"""Umbrella ``ofp`` command-line interface.

``ofp`` is a thin dispatcher over the Object-flow Programming Language toolchain.
It forwards each subcommand to a sibling package's own CLI, in-process::

    ofp validate ...  ->  ofplang.validate.cli.main
    ofp schedule ...  ->  ofplang.schedule.cli.main
    ofp run ...       ->  ofplang.run.cli.main

Each subcommand keeps its own options, exit codes, and ``--help``; ``ofp`` adds
no behavior of its own beyond routing plus a top-level ``--help``/``--version``.
"""

from __future__ import annotations

import importlib
import sys
from collections.abc import Sequence

# Subcommand -> dotted path of the sibling CLI module exposing ``main(argv)``.
# Kept as strings so each sibling is imported lazily, only when its subcommand is
# invoked: ``ofp --help`` need not import a scheduler's ortools/numpy stack, and a
# subcommand fails with a clear message if its package is somehow missing.
_SUBCOMMANDS: dict[str, str] = {
    "validate": "ofplang.validate.cli",
    "schedule": "ofplang.schedule.cli",
    "run": "ofplang.run.cli",
}

_USAGE = """\
usage: ofp <command> [options]

The umbrella CLI for the Object-flow Programming Language toolchain.

commands:
  validate    check a workflow document is well-formed portable v0
  schedule    compute a schedule for a workflow
  run         execute a workflow (rolling-horizon runner / simulator)

Run `ofp <command> --help` for command-specific options.

options:
  -h, --help     show this help and exit
  -V, --version  show version and exit
"""


def _version() -> str:
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version("ofplang")
    except PackageNotFoundError:  # editable/source tree without installed metadata
        return "0+unknown"


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if not args:
        sys.stderr.write(_USAGE)
        return 2

    head = args[0]
    if head in ("-h", "--help"):
        sys.stdout.write(_USAGE)
        return 0
    if head in ("-V", "--version"):
        sys.stdout.write(f"ofp {_version()}\n")
        return 0
    if head.startswith("-"):
        sys.stderr.write(f"ofp: unrecognized option {head!r}\n\n")
        sys.stderr.write(_USAGE)
        return 2

    module_path = _SUBCOMMANDS.get(head)
    if module_path is None:
        sys.stderr.write(f"ofp: unknown command {head!r}\n\n")
        sys.stderr.write(_USAGE)
        return 2

    try:
        module = importlib.import_module(module_path)
    except ImportError as exc:
        sys.stderr.write(
            f"ofp: the '{head}' command requires a package that is not installed "
            f"({exc}).\n"
        )
        return 2

    exit_code: int = module.main(args[1:])
    return exit_code
