# ofplang

[![CI](https://github.com/ofplang/ofp/actions/workflows/ci.yml/badge.svg)](https://github.com/ofplang/ofp/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/ofplang.svg)](https://pypi.org/project/ofplang/)

The umbrella **`ofp`** command-line interface for the **Object-flow Programming
Language** toolchain. Installing this one package pulls in the whole toolchain
and exposes it under a single command:

```sh
ofp validate ...   # check a workflow is well-formed portable v0
ofp schedule ...   # compute a schedule for a workflow
ofp run ...        # execute a workflow (rolling-horizon runner / simulator)
```

The language is defined in the [ofplang/spec](https://github.com/ofplang/spec)
repository.

## Install

```sh
pip install ofplang
```

Requires Python 3.10+. This package is a thin dispatcher; it depends on the
sibling packages that do the work:

- [`ofplang-validate`](https://github.com/ofplang/validate) — the validator
- [`ofplang-schedule`](https://github.com/ofplang/schedule) — the scheduler
- [`ofplang-run`](https://github.com/ofplang/run) — the runner / simulator

## Command line

```sh
ofp <command> [options]         # or: python -m ofplang.ofp <command> [options]
ofp <command> --help            # command-specific options
ofp --version
```

`ofp` forwards each subcommand to the corresponding sibling CLI **in-process**,
so every command keeps its own options, output, and exit codes. `ofp` itself
adds only routing and a top-level `--help`/`--version`.

Each sibling also installs its own standalone command (`ofp-validate`,
`ofp-schedule`, `ofp-run`); `ofp <command>` is the convenience aggregator.

Exit codes: `2` for an unknown/missing command or usage error at the `ofp`
level; otherwise the subcommand's own exit code is returned unchanged.

## Scope

This repository contains only the dispatcher. Behavior, options, and semantics
live in the sibling repositories linked above. The package is published to PyPI
as `ofplang`; the `ofplang` import namespace is a PEP 420 namespace shared
across the organization's tools, and this distribution provides `ofplang.ofp`.
