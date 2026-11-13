# CI/CD skill
1. Run formatting, lint, unit tests and type checks on every pull request.
2. Add secret scanning and dependency auditing before artifact publication.
3. Pin runtime versions and resolve dependencies from committed lockfiles.
4. Build immutable artifacts once; promote the same artifact across environments.
5. Require explicit approval for production deployment and use health checks plus rollback.
6. Do not store credentials in logs, workflow files or repository variables with broader scopes than required.
