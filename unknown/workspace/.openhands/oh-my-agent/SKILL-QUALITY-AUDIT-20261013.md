# Skill File Quality Inventory — 2026-10-13

Scope: static metadata audit of `/root/workspace/.agents/skills`. This does not execute skills or prove correctness, safety, license, or runtime compatibility.

- Skill directories: **134**
- Non-empty `SKILL.md`: **134**
- YAML-style frontmatter present: **94**
- No frontmatter detected: **40**
- `SKILL.md` under 500 bytes: **57**
- `README.md` present: **71**
- Directory name found in `SOURCES.md`: **132**

A directory-name match in `SOURCES.md` is only a weak provenance signal; the source manifest must be reviewed item by item. Short files are not automatically invalid, but require checking whether they contain complete actionable instructions.

| Skill | SKILL.md bytes | Lines | Frontmatter | README | Name in source manifest | SHA-256 |
|---|---:|---:|---|---|---|---|
| `add-javadoc` | 1166 | 35 | yes | yes | yes | `93422a18b7d6a98e…` |
| `add-skill` | 2243 | 52 | yes | yes | yes | `dfe7467e03adfcbc…` |
| `agent-canvas-environment` | 9959 | 202 | yes | yes | yes | `40562401fb3e07a9…` |
| `agent-creator` | 7254 | 190 | yes | yes | yes | `c7321d4a60420cef…` |
| `agent-fleet-secure-workflow` | 3560 | 36 | yes | no | no | `b95eb16119f10aa5…` |
| `agent-memory` | 2051 | 30 | yes | yes | yes | `f91fb602088b1473…` |
| `agent-readiness-report` | 4477 | 124 | yes | yes | yes | `e11eafa6fa0be079…` |
| `agent-sdk-builder` | 2849 | 37 | yes | yes | yes | `0085981836b18cd8…` |
| `agent-skills` | 307 | 8 | yes | no | yes | `b3fe06b898534b82…` |
| `agentic-security-review` | 3912 | 36 | yes | no | no | `5e0117bf01d205d2…` |
| `api-compatibility` | 2238 | 36 | yes | no | yes | `71a3abafda738e30…` |
| `api-integration` | 143 | 7 | no | no | yes | `5aa329eb24fac2f3…` |
| `apollo-memory` | 289 | 8 | yes | no | yes | `8ee231c3f7e5f126…` |
| `auth-security` | 139 | 7 | no | no | yes | `5e4e917e1b0268ff…` |
| `automated-ui-asset-generator` | 169 | 7 | no | no | yes | `ed2abbfbc437f732…` |
| `azure-devops` | 3552 | 61 | yes | yes | yes | `df602c5dc300b53b…` |
| `bitbucket` | 2551 | 56 | yes | yes | yes | `b9c7fb63cef358d8…` |
| `bitbucket-cloud` | 3878 | 57 | yes | yes | yes | `05fa500943fea494…` |
| `bitbucket-data-center` | 3634 | 53 | yes | yes | yes | `912dd5497f8bd360…` |
| `BrowserGym` | 122 | 6 | no | no | yes | `3c0f4b01e4eabf3d…` |
| `build-your-own-x` | 340 | 12 | no | no | yes | `dcc1574c2e0b8814…` |
| `canvas-extension-api` | 20315 | 285 | yes | yes | yes | `7f9d2cd77059b51d…` |
| `cc-suite-bridge` | 143 | 7 | no | no | yes | `bd3eea391fafc305…` |
| `ci-cd-pipeline` | 141 | 7 | no | no | yes | `a7756aa158cf7e44…` |
| `CI-CD-Watcher` | 128 | 6 | no | no | yes | `ee0cd108b6904713…` |
| `cluster-load-balancer` | 155 | 7 | no | no | yes | `f2cfa528b53a626a…` |
| `code-review` | 8455 | 174 | yes | yes | yes | `f4a3bf947db539fb…` |
| `code-simplifier` | 5033 | 91 | yes | yes | yes | `ba5cfc2908e5d7e4…` |
| `composio` | 248 | 8 | yes | no | yes | `4ad334953f841c6b…` |
| `composio-tool-integration` | 266 | 8 | yes | no | yes | `84da1bab9c5f8ffd…` |
| `cross-repo-testing` | 9933 | 202 | yes | no | yes | `bdb1abf40b029711…` |
| `datadog` | 2864 | 97 | yes | yes | yes | `c67db102d293d21e…` |
| `db-migrate` | 133 | 7 | no | no | yes | `31ab554e7a13f865…` |
| `DB-Schema-Grapher` | 136 | 6 | no | no | yes | `ad36f2cf663d17d0…` |
| `deep-packet-inspector` | 155 | 7 | no | no | yes | `51661ee8ab021f23…` |
| `define-to-ship` | 264 | 8 | yes | no | yes | `e327e2ec4c2343d5…` |
| `deno` | 2266 | 99 | yes | yes | yes | `6704eb29264daea9…` |
| `dependency-resolver` | 151 | 7 | no | no | yes | `d3137adb3ea477f7…` |
| `discord` | 4352 | 111 | yes | yes | yes | `ff1cc68562cddeb1…` |
| `docker` | 922 | 33 | yes | yes | yes | `d4c69e41982982cf…` |
| `docker-orchestration` | 153 | 7 | no | no | yes | `8cc8680dbc6907b2…` |
| `Docker-Sandbox-Plus` | 140 | 6 | no | no | yes | `11a8abfd1a727210…` |
| `documentation-gen` | 147 | 7 | no | no | yes | `842307d355fc312f…` |
| `ecc` | 270 | 8 | yes | no | yes | `da47de1ffc93be22…` |
| `engineering-memory` | 346 | 8 | yes | no | yes | `95a10a5bb9e1ff5e…` |
| `env-verifier` | 137 | 7 | no | no | yes | `8d5eff1678e0bc62…` |
| `evidence-based-citations` | 3182 | 59 | yes | yes | yes | `ebd2645e8e365121…` |
| `evolution-tree` | 399 | 4 | no | no | yes | `81644fefcd628232…` |
| `ffmpeg-media-matrix` | 151 | 7 | no | no | yes | `974f871fb1f85256…` |
| `firecrawl` | 254 | 8 | yes | no | yes | `0d11012d4936b241…` |
| `firecrawl-web-research` | 271 | 8 | yes | no | yes | `ac34e8b9732edf9b…` |
| `flarglebargle` | 337 | 9 | yes | yes | yes | `4abf0757e97eeb11…` |
| `frontend-design` | 4443 | 42 | yes | yes | yes | `982cecaaf2a95a76…` |
| `full-cycle-mobile-dev` | 1476 | 24 | no | no | yes | `66dda4f1708e6c23…` |
| `git-commander` | 139 | 7 | no | no | yes | `076d7d4eb106599d…` |
| `Git-Flow-Manager` | 134 | 6 | no | no | yes | `7fda30927083063e…` |
| `github` | 4880 | 107 | yes | yes | yes | `c618546605a8461d…` |
| `github-actions` | 1888 | 44 | yes | yes | yes | `3bc9316152997400…` |
| `github-agents-md-maintainer` | 11745 | 277 | yes | yes | yes | `a117d2f599af00a8…` |
| `github-delivery-watchdog` | 1952 | 35 | yes | yes | yes | `536cb76358c784e8…` |
| `github-issue-to-pr` | 17616 | 387 | yes | yes | yes | `602425d9c99c774e…` |
| `github-issue-triage` | 3141 | 57 | yes | yes | yes | `eec8e8f6d1c9f41f…` |
| `github-pr-review` | 9137 | 197 | yes | yes | yes | `8b1c2f74dede90bb…` |
| `github-pr-reviewer` | 26054 | 498 | yes | yes | yes | `d35abc63129f9a34…` |
| `github-repo-monitor` | 12247 | 323 | yes | yes | yes | `8a51a228f4a37216…` |
| `github-stale-ci-pr-closer` | 1210 | 24 | yes | yes | yes | `060b136307daf00b…` |
| `gitlab` | 2164 | 33 | yes | yes | yes | `214c4db1a10ec41b…` |
| `gitlab-issue-to-mr` | 18988 | 408 | yes | yes | yes | `95b4390e73cc3ba6…` |
| `go-microservices-generator` | 165 | 7 | no | no | yes | `11ad92e05fb9197e…` |
| `harness-evolution` | 260 | 8 | yes | no | yes | `3024dd7eaa24a47a…` |
| `improve-agent-readiness` | 6657 | 167 | yes | yes | yes | `e34bcd869080b07a…` |
| `incident-retrospective` | 3554 | 100 | yes | yes | yes | `bf99ca3938e3245b…` |
| `iterate` | 15153 | 420 | yes | yes | yes | `58249391292da7a9…` |
| `jira-issue-to-pr` | 10124 | 216 | yes | yes | yes | `e5c143d6c0256e7c…` |
| `jupyter` | 1540 | 56 | yes | yes | yes | `11f5663bd9bc3298…` |
| `kubernetes` | 1303 | 49 | yes | yes | yes | `e1c28130b212211c…` |
| `large-codebase` | 141 | 7 | no | no | yes | `014d3630c9d3c892…` |
| `learn-from-code-review` | 6300 | 186 | yes | yes | yes | `146a6ec992965016…` |
| `linear` | 7151 | 215 | yes | yes | yes | `f0a509cc3268de2d…` |
| `linear-triage` | 3045 | 93 | yes | yes | yes | `4a6dfb4a604c9958…` |
| `log-analyzer` | 137 | 7 | no | no | yes | `6694c366425c7f3e…` |
| `magic-word` | 910 | 34 | yes | no | yes | `4e57df560848c006…` |
| `memory-leak-plugger` | 151 | 7 | no | no | yes | `f4edbd4daf4aaa82…` |
| `multimodal-mcp-adapter` | 213 | 4 | no | no | yes | `2664f1a4edacfa4a…` |
| `news-digest` | 12278 | 284 | yes | yes | yes | `833aace23ab5b4a5…` |
| `notion` | 3786 | 111 | yes | yes | yes | `2ae4b3833a317815…` |
| `npm` | 440 | 9 | yes | yes | yes | `f29251d112f6ba93…` |
| `npm-conflict-resolver` | 144 | 6 | no | no | yes | `4131f8e32868e7ad…` |
| `obra-superpowers` | 299 | 8 | yes | no | yes | `df15628960ad0ceb…` |
| `openhands-api` | 18282 | 469 | yes | yes | yes | `f0124b4e04066b3b…` |
| `openhands-automation` | 41399 | 904 | yes | yes | yes | `19a7315f0d171500…` |
| `openhands-enterprise-troubleshooting` | 15206 | 339 | yes | yes | yes | `b7baa048b8fbcbb9…` |
| `openhands-sdk` | 27349 | 248 | yes | yes | yes | `033b9e64ec7639f4…` |
| `OSWorld-Core` | 126 | 6 | no | no | yes | `77e991dbc1a0d95b…` |
| `package-cleaner` | 143 | 7 | no | no | yes | `0854fe1590fa4d6d…` |
| `pdflatex` | 1278 | 36 | yes | yes | yes | `cf92e9e088dffea0…` |
| `performance-tuner` | 147 | 7 | no | no | yes | `f73904255c8f1eaf…` |
| `plain-english-content` | 6023 | 78 | yes | yes | yes | `2ef939ec154a2555…` |
| `plan-once-verify-always` | 285 | 8 | yes | no | yes | `01846ad0441d08e9…` |
| `prd` | 6897 | 237 | yes | yes | yes | `5de2431f9ceb205f…` |
| `Pytest-AutoHealing` | 138 | 6 | no | no | yes | `f7dcbd57ea76d37b…` |
| `python-bytecode-optimizer` | 163 | 7 | no | no | yes | `74a9392b9b0465e4…` |
| `qa-changes` | 14712 | 229 | yes | yes | yes | `e4819ced02fce8f1…` |
| `release-notes` | 854 | 19 | yes | yes | yes | `5250f2d1aa52272a…` |
| `research-brief` | 3186 | 101 | yes | yes | yes | `662a6bf42ec9964b…` |
| `rust-wasm-compiler` | 149 | 7 | no | no | yes | `a68f8208132f9a39…` |
| `security` | 1367 | 33 | yes | yes | yes | `887a8c46466e3886…` |
| `self-evolving-engineer` | 435 | 2 | no | no | yes | `1784cbb8d01b48c5…` |
| `sesm-engine` | 261 | 8 | yes | no | yes | `1141bcaa3edc8462…` |
| `setup-agents-md` | 6035 | 150 | yes | yes | yes | `33abece9c9e27263…` |
| `setup-openhands` | 2222 | 56 | yes | yes | yes | `1c2381e0c1547d3c…` |
| `setup-pr-review` | 2939 | 72 | yes | yes | yes | `70b8d5fb44619412…` |
| `skill-creator` | 20969 | 546 | yes | yes | yes | `651c6a4db39a16d3…` |
| `skill-optimizer` | 262 | 8 | yes | no | yes | `a0017c12f79d429a…` |
| `slack-channel-monitor` | 12730 | 305 | yes | yes | yes | `2699798becdf629b…` |
| `Slack-Notifier-Agent` | 142 | 6 | no | no | yes | `8053e0a45086684a…` |
| `slack-standup-digest` | 3208 | 94 | yes | yes | yes | `58e779cdde7f0029…` |
| `SonarQube-Linter` | 134 | 6 | no | no | yes | `4d2b316953c942a5…` |
| `spark-version-upgrade` | 7777 | 234 | yes | yes | yes | `4351d37aec3b7b19…` |
| `ssh` | 3371 | 136 | yes | yes | yes | `ca7cca10ed32ca28…` |
| `swift-linux` | 2637 | 82 | yes | yes | yes | `e4c39d4cfd04335d…` |
| `technical-writing` | 4888 | 106 | yes | yes | yes | `ddd627776d70161f…` |
| `theme-factory` | 3124 | 59 | yes | yes | yes | `c35893e221e28895…` |
| `ticket-to-code-change` | 2278 | 50 | yes | yes | yes | `1d063f120e1238da…` |
| `understand-anything` | 271 | 8 | yes | no | yes | `69357ecae8cb1a76…` |
| `unit-testing` | 137 | 7 | no | no | yes | `2d26ed7107e968e3…` |
| `upcoming-release` | 1188 | 37 | yes | no | yes | `5b0fee629f2e84b4…` |
| `update-sdk` | 6294 | 123 | yes | no | yes | `6a8222dc0b65d6a0…` |
| `upstream-fork-sync` | 4606 | 122 | yes | yes | yes | `c53faa66ce41f084…` |
| `uv` | 2639 | 95 | yes | yes | yes | `e321822ec05752b5…` |
| `vercel` | 3240 | 108 | yes | yes | yes | `4060634017206b72…` |
| `vps-bridge` | 255 | 8 | yes | no | yes | `e3dd74915dc69efe…` |
| `vulnerability-remediation` | 163 | 7 | no | no | yes | `d4b480e258c2d6d8…` |
| `zero-knowledge-proof-auth` | 163 | 7 | no | no | yes | `7e5e759625b7be5b…` |
