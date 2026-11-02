---
name: api-compatibility
description: Configure and verify OpenAI-compatible and Anthropic-compatible provider access through the shared LiteLLM gateway without duplicating agents or exposing credentials.
---

# API Compatibility

## Shared gateway contract

- Default OpenAI-compatible endpoint: http://127.0.0.1:4000/v1
- OpenHands container bridge: http://host.docker.internal:4001/v1
- Anthropic Messages endpoint base: http://127.0.0.1:4000
- Gateway key environment variable: LITELLM_MASTER_KEY
- Default low-cost local model alias: my-model
- Never commit credentials. Read them from the root-only environment file or a secret manager.
- Keep model aliases identical across agents. Do not claim a provider model is active unless the gateway model catalog lists it.
- Keep existing provider entries and user configuration. Add missing entries; do not overwrite or delete unrelated settings.
- Distinguish configured, discoverable, inference-tested, and end-to-end verified states.

## Verification sequence

1. Confirm the canonical LiteLLM service is active and only one service owns port 4000.
2. Confirm the bridge is reachable only from the authorized Docker bridge network.
3. Request the model catalog with the configured gateway key and confirm the requested alias is present.
4. Confirm unauthenticated requests are rejected; never print key material.
5. Test the provider-specific chat protocol only in an approved test mode and record the response status and model alias.
6. For external providers, verify key presence and model catalog configuration without triggering paid inference unless explicitly authorized.
7. Back up configuration before changes and record rollback instructions.

## Protocol notes

- OpenAI-compatible agents use the /v1 endpoint and the gateway key.
- Claude Code uses the Anthropic Messages protocol at the gateway base URL, not the OpenAI /v1 URL.
- OpenHands uses the private host bridge; its container must have a scoped firewall allowance to the bridge.
- ACP-only agents require their own provider adapter. An environment file alone is not proof that the ACP runtime loaded it.
- Messaging, tool-only, disabled, or manual-only services are not automatically converted into LLM agents.
