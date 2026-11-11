# Repository migration skill

1. Inventory repository path, owner, origin/upstream URLs, branch, HEAD SHA, dirty state, staged changes, untracked files, submodules, LFS and size.
2. Do not fetch or restore credentials from a deleted GitHub account. Public upstreams may be fetched independently.
3. Preserve uncommitted work. Create a read-only backup or migration branch before changing remotes.
4. Scan tracked files, untracked files, staged diff and Git history for secrets. Classify test fixtures separately from live credentials.
5. Exclude .env, key files, private data, runtime databases, caches, build output and model weights.
6. Reconcile nested repositories and submodules explicitly; never flatten them implicitly.
7. Test/build the exact project.
8. Push only to an explicitly selected 0megAlpha repository using normal commits; verify remote SHA and tree contents.
9. Record source, destination, commit SHA, excluded paths and test evidence.
