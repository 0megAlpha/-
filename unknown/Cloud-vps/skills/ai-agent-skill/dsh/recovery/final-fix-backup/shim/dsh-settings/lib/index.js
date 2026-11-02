// Compatibility shim for dsh 0.1.5-rc.2.
//
// The real @deepseek-ai/dsh-settings (from the dsh installation, reached via
// the shared $DSH_HOME/profiles/node_modules module fallback) does not export
// the legacy `settingsNamespace` named export — it was removed in 0.1.2-rc.1.
// Plugins built against the older API (dsh-at-file@0.6.x,
// dsh-tool-describe-image@0.5.x) still do `import { settingsNamespace } from
// "@deepseek-ai/dsh-settings"`. The old helper was identity-with-validation,
// and its result is passed straight into the rc.2 `settings.register(ns, …)`
// API which accepts the plain string, so the re-export below is fully
// compatible with the current settings service.
//
// This file is generated; a future `pnpm install` in this profile may replace
// this directory with the package pnpm resolves — regenerate if needed.

export {
  SettingsConflictError,
  SettingsProvider,
  redactSecrets,
} from "../../../../../node_modules/@deepseek-ai/dsh-settings/lib/index.js";
export { default } from "../../../../../node_modules/@deepseek-ai/dsh-settings/lib/index.js";

export function settingsNamespace(value) {
  if (typeof value !== "string" || !/^[a-z][a-z0-9-]*$/.test(value)) {
    throw new TypeError(
      `settings namespace "${value}" must match /^[a-z][a-z0-9-]*$/`,
    );
  }
  return value;
}