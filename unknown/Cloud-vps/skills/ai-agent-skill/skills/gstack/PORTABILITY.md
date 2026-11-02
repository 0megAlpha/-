# gstack source and portability notes

- Upstream repository: https://github.com/garrytan/gstack
- Snapshot package version: 1.87.4 (from package.json)
- License: MIT; see LICENSE. Preserve the upstream copyright and license notice.
- This VPS snapshot may contain local changes; an upstream commit SHA has not been verified. Compare against upstream before updating or claiming exact upstream parity.
- Supabase project values were removed from supabase/config.sh. Supply GSTACK_SUPABASE_URL and GSTACK_SUPABASE_ANON_KEY via local environment or an untracked secret file; .env.example contains nonfunctional placeholders only.
- Do not commit local sessions, tokens, private keys, or runtime databases. Build generated assets from source where the upstream build procedure supports it.
