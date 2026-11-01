# VPS Mirror Runbook (mobile-first)

Target: private repository `0megAlpha/-`  
Current inventory branch: `vps-mirror/inventory-2026-11`

This runbook explains the safe way to materialize the Agent sources for browsing and to migrate VPS-local modifications. A Git submodule is a pointer to another repository; it does not embed that repository's files into the parent tree. A clone using `--recurse-submodules` checks out those source repositories. If the requirement is that every file is visible as an ordinary folder inside one GitHub repository, use the separate full-tree branch and Git subtree workflow below.

## A. Open and browse on an iPhone

1. Open the inventory branch in Safari:
   `https://github.com/0megAlpha/-/tree/vps-mirror/inventory-2026-11`
2. GitHub submodule entries are links. Tap the entry to open the upstream repository. The parent repository page shows the pinned commit, not the entire submodule file list.
3. For browser editing of ordinary files, change the URL host from `github.com` to `github.dev`. VS Code for the Web runs in the browser and is useful for lightweight edits. It is not a full build terminal and keeps edits in browser storage until committed; commit often.
4. For a full browser VS Code terminal/build environment, use GitHub `Code` → `Codespaces` → create a codespace on `vps-mirror/inventory-2026-11`. Codespaces availability, billing and included usage depend on the GitHub account plan.
5. Replit is another connected browser IDE. Import the private repository through its GitHub integration. Do not assume submodules are fetched automatically; use its shell to run `git submodule update --init --recursive` and verify each submodule.

## B. Materialize the existing submodule sources on the VPS

Use Termius to SSH to the VPS as `xiaye` and run:

```bash
mkdir -p "$HOME/agent-mirror"
git clone --recurse-submodules \
  --branch vps-mirror/inventory-2026-11 \
  https://github.com/0megAlpha/-.git \
  "$HOME/agent-mirror/central"
cd "$HOME/agent-mirror/central"
git submodule status --recursive
```

If HTTPS asks for credentials, authenticate interactively or use a short-lived credential helper; never put a token into the clone URL, shell history, a script, or a Git config file committed to the repository. The parent is private, so GitHub authentication must be for an account with access to `0megAlpha/-`.

## C. Credentials needed for the actual VPS migration

The current Gateway `github-mirror-credential` is an environment secret and has been used successfully for public upstream fetches. The VPS private source origins `xh09411-web/Ai-agent-skill`, `xh09411-web/Claude-code` and `xh09411-web/Google-AI` returned GitHub 404/not accessible. This is usually a repository-owner/access-selection issue, not a Git command issue.

Use two credentials where the source and target owners differ:

- Source-read credential: create a fine-grained PAT for the account/organization that owns the private source repos; select `Ai-agent-skill`, `Claude-code`, `Google-AI` and any other private source repos; grant Repository Contents: Read and Metadata: Read. Store it in Gateway as `github-source-credential`, purpose `environment`.
- Target-write credential: keep `github-mirror-credential` scoped to owner `0megAlpha`, repository `-`; grant Contents: Read and write and Metadata: Read. Add Workflows: Read and write only if updating `.github/workflows/*.yml` files.
- If the source repos are owned by a different account, that account must grant the token owner read access (or add that account as a collaborator). A target-only token cannot read unrelated private repositories.
- Never paste tokens/passwords into ChatGPT. Enter them only in Gateway's secret form.

Gateway sudo setup: `https://trygateway.sh/app/servers/srv_01M691XRH300JR2KZND0ZJPF3S/sudo`. Choose one-time or time-limited sudo if the tool reports action required. Do not grant blanket passwordless root permanently just for convenience.

## D. Full-tree layout versus submodules

The current inventory branch intentionally uses submodule references for public upstream projects. To make the code itself appear as ordinary folders inside one repository, create a separate branch named `vps-mirror/full-tree` from the inventory branch. Do not overwrite the inventory branch.

In a fresh clone of the parent repository **without** initializing submodules:

```bash
git clone --branch vps-mirror/inventory-2026-11 \
  https://github.com/0megAlpha/-.git "$HOME/agent-mirror/full-tree"
cd "$HOME/agent-mirror/full-tree"
git switch -c vps-mirror/full-tree
git submodule status
```

Before replacing pointers, confirm this fresh clone has no initialized submodule worktrees. List the gitlinks with:

```bash
git ls-files --stage | awk '$1 == "160000" {print $4, $2}'
```

Only after verifying the paths are the intended pointers and the checkout contains no local submodule edits, remove the gitlinks in this new branch, remove the matching sections from `.gitmodules`, commit that branch change, and import the actual upstream content with `git subtree add` (do not use `--squash` when preserving complete commit history):

```bash
git rm --cached -- hermes CKA-Agent \
  openhands/core openhands/extensions openhands/software-agent-sdk
# Edit .gitmodules and remove the five matching submodule sections, then:
git add .gitmodules
git commit -m "mirror: convert upstream pointers to full source folders"

git subtree add --prefix=hermes \
  https://github.com/NousResearch/hermes-agent.git main

git subtree add --prefix=openhands/core \
  https://github.com/OpenHands/OpenHands.git main

git subtree add --prefix=openhands/software-agent-sdk \
  https://github.com/OpenHands/software-agent-sdk.git main

git subtree add --prefix=openhands/extensions \
  https://github.com/OpenHands/extensions.git main

git subtree add --prefix=CKA-Agent \
  https://github.com/Graph-COM/CKA-Agent.git main

git push origin vps-mirror/full-tree
```

This branch conversion must be done on a fresh clone and only after the gitlinks and `.gitmodules` paths have been checked. If `git subtree` is unavailable, install the distro's Git subtree package from the official package source, then verify `git subtree -h` before continuing.

## E. Preserve VPS-local changes before importing them

Do not pull/rebase/reset a dirty source repository. For each source repository:

1. Record `git status --short --branch`, remotes, all branches and recent commits.
2. Create a backup bundle of committed refs: `git -C SOURCE bundle create BACKUP.bundle --all`. Store it outside the project tree with restricted permissions.
3. Preserve staged and unstaged deltas separately: `git diff --cached --binary` and `git diff --binary`; list untracked paths using `git ls-files --others --exclude-standard`.
4. Create a separate migration worktree/branch from the current HEAD. Apply the combined `git diff HEAD --binary` patch there, then copy only reviewed, non-secret untracked source files into it. Do not change the original worktree.
5. Scan the migration tree and Git history for secrets before staging. Exclude `.env*`, tokens, API keys, private keys, SSH files, credential stores, session data, databases, secret-bearing logs, virtualenvs, `node_modules`, caches, generated model weights and build output. Keep a manifest of exclusions.
6. Commit the reviewed snapshot to the migration branch, then import it into the parent with `git subtree add --prefix=DESTINATION LOCAL_REPO MIGRATION_BRANCH`. This preserves the source commit history and makes the files ordinary files below the destination folder.
7. Push the parent `vps-mirror/full-tree` branch; never force-push the inventory branch or the source project's existing branch.

For a repo with staged changes already present (Google-AI has 2,563 staged paths), `git diff HEAD` captures the final tracked worktree delta relative to HEAD, but untracked paths still require a separate review/copy. Inspect `.gitmodules` and submodule gitlinks before snapshotting. Do not blindly commit that staged state onto the existing `main` branch.

## F. Destination map

| VPS source | Full-tree folder |
|---|---|
| `/home/xiaye/Ai-agent-skill` | `Ai-agent-skill/` |
| `/home/xiaye/repository/Google-AI` | `Google-AI/` |
| `/home/xiaye/Claude-code` | `Claude-code/` |
| `/home/xiaye/hermes-007` | `hermes/` (merge the VPS-local export into the upstream base after backup) |
| `/home/xiaye/openhands-extensions` | `openhands/extensions/` |
| `/opt/open-hands-integrated-main` | `openhands/integrated/` |
| `/opt/openhands-upstream-build-v1.25.0` | `openhands/upstream-build-v1.25.0/` |
| `/opt/hermes-agent-v0.22.5` | `hermes/installed-v0.22.5/` only if confirmed as distinct source, otherwise inventory it separately |
| `/home/xiaye/CKA-Agent` | `CKA-Agent/` |
| `/home/xiaye/All-in` | `All-in/` |
| `/opt/agent-plane` | `agent-plane/` |
| `/opt/sentinelx-cloud-core` | `sentinelx-cloud-core/` |
| `/home/xiaye/ai-agent-fleet` | `ai-agent-fleet/` |
| `/opt/openwebui-plugins` | `openwebui-plugins/` |

Other root-level Agent directories without confirmed identity stay in `VPS-AGENT-INVENTORY.md` until their relationship and destination are known.

## G. Final verification checklist

- `git submodule status --recursive` (on the submodule branch) or confirm all source directories are regular trees (on the full-tree branch).
- Confirm all expected destination folders are present.
- Compare source and destination file inventories and SHA-256 for every approved file; record exclusions.
- Check each source repo HEAD, branch, tags and the imported migration commit.
- Verify that no `.env`, credentials, private keys, runtime databases or unreviewed secret files were committed.
- Run project-specific tests/builds in isolated environments; a folder existing is not proof the agent can run.
- Validate agent model/API integration with a configurable OpenAI-compatible `base_url` (e.g. the existing LiteLLM endpoint), separate per-agent keys, model aliases and budgets. Store all provider secrets outside Git.
- Verify MCP/plugin manifest, required environment-variable names, health endpoint, startup command and browser access for each Agent.
- Only then label a project `mirrored + updated + build-verified + runtime-verified`.

## H. Known blockers from latest VPS checks

- Public upstream fetch succeeded for Hermes, OpenHands Extensions (31 remote-tracking refs updated), and CKA-Agent (0 refs changed).
- The private remotes under `xh09411-web` returned repository-not-found for the current Gateway credential.
- `Ai-agent-skill`: one local commit ahead / 24 behind, modified `push.sh`, seven untracked paths.
- `Google-AI`: 2,563 staged paths and an OpenHands gitlink; do not commit/reset on the original branch.
- Hermes has two untracked secrets-guide directories; inspect before inclusion.
- CKA-Agent has a modified config and a backup.
- Shellway currently has no paired computers; SentinelX has no enrolled hosts; Termalin Pro access has expired. These are not blockers for GitHub source mirroring while Gateway SSH is available.
