# Skill source inventory

## gstack

- Path: `skills/gstack/`
- Upstream: https://github.com/garrytan/gstack
- Snapshot package version: `1.87.4` (from `package.json`)
- License: MIT; see `skills/gstack/LICENSE`.
- Caveat: the exact upstream commit was not verified for this VPS snapshot. Compare with upstream before updating or claiming exact upstream parity.
- Portability change: project-specific Supabase URL and anon key values were removed from `supabase/config.sh`. Supply `GSTACK_SUPABASE_URL` and `GSTACK_SUPABASE_ANON_KEY` through the environment or an untracked local secret file. `supabase/.env.example` contains nonfunctional placeholders.

## Existing skills

Skills already tracked in the canonical repository remain unchanged by this import. For future additions, record the source repository and license evidence; do not redistribute content with unknown provenance or incompatible license terms.
