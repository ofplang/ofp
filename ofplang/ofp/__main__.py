"""Enable ``python -m ofplang.ofp <command> ...``.

Intent: mirror the console-script entry point so the CLI is reachable without an
installed script, which is convenient in dev checkouts and CI.
"""

from ofplang.ofp.cli import main

raise SystemExit(main())
