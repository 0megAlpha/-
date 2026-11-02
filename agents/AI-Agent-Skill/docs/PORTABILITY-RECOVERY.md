
## Portability pass 2026-10-09
- Runtime boundaries added under `runtimes/`; source repositories remain independent and are reproducible via `runtime-sources.yaml` + `bootstrap.sh`.
- Evolution tree added under `evolution-tree/`; production promotion requires sandbox evaluation, verification, versioning and rollback.
- OpenHands 1.25.0 Agent Canvas image pulled successfully and preserved as a side-by-side migration candidate; production 0.14 container was not replaced because the new image did not yet pass endpoint verification.
- Hermes Agent remains on the previously verified 0.21.6 upstream-synced build.
