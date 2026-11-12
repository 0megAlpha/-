# Browser testing skill
Use Playwright Test in the target web repository, pinned through that repository's package manager lockfile.
1. Identify the app's existing local/staging URL; never publish a new listener just for tests.
2. Add deterministic tests for navigation, primary flows, accessibility semantics and responsive layouts.
3. Use role/label/test-id locators; avoid brittle CSS selectors and arbitrary sleeps.
4. Capture screenshots, traces and console/network errors on failure; redact cookies, tokens and user data.
5. Run Chromium first, then additional browsers only when required by the project's support matrix.
6. Keep browser binaries and artifacts out of Git; upload only sanitized reports.
