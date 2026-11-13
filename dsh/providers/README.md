# DSH Provider Adapter

Keep DSH profiles, plugins and skills in the DSH directory. Configure the active profile to use either its native provider or an OpenAI-compatible endpoint supported by the installed DSH version.

- `OPENAI_BASE_URL`: API root, normally `/v1`
- `OPENAI_API_KEY`: runtime credential
- `DSH_MODEL`: model alias registered at the endpoint

See `dsh.env.example`. Verify with the DSH profile's own model test before marking the provider live.
