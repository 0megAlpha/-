# Reviewed secret-scan exceptions

These exact Gitleaks fingerprints were reviewed on 2026-10-11 for the vendored MIT-licensed `wshobson/agents` marketplace. No secret values are reproduced here.

| Fingerprint path | Rule | Review result |
|---|---|---|
| `agents/marketplace/plugins/code-documentation/commands/doc-generate.md:555` | `curl-auth-header` | Documentation example with a placeholder-style auth header; no live credential found. |
| `agents/marketplace/plugins/documentation-generation/commands/doc-generate.md:555` | `curl-auth-header` | Duplicate documentation example with a placeholder-style auth header; no live credential found. |
| `agents/marketplace/plugins/plugin-eval/src/plugin_eval/layers/static.py:383` | `generic-api-key` | False positive on static-analysis implementation/docstring; no credential literal found. |

The allowlist is limited to these exact path/rule/line fingerprints. If files move or lines change, re-review new findings instead of broadening the ignore patterns.
