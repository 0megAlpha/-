/**
 * Unit tests for lib/redact-engine.ts + lib/redact-patterns.ts.
 *
 * One positive test per pattern, plus FP-filters, validators (Luhn/entropy/
 * RFC1918), email allowlist, no-promotion visibility semantics, tool-fence
 * degrade, normalization (zero-width / homoglyph / entity), oversize fail-closed,
 * and pure-function purity.
 */
import { describe, test, expect } from "bun:test";
import {
  scan,
  exitCodeFor,
  maskPreview,
  normalizeWithMap,
  redactFindingSpans,
  type RepoVisibility,
} from "../lib/redact-engine";
import {
  PATTERNS,
  luhnValid,
  shannonEntropy,
  isPublicIPv4,
  isPlaceholderSpan,
  URL_PASSWORD_PLACEHOLDER_WORDS,
} from "../lib/redact-patterns";

function ids(text: string, vis: RepoVisibility = "private"): string[] {
  return scan(text, { repoVisibility: vis }).findings.map((f) => f.id);
}

describe("HIGH credential patterns", () => {
  const cases: Array<[string, string]> = [
    ["aws.access_key", "key = [REDACTED_BY_GATEKEEPER]"],
    ["aws.secret_key", "aws_secret_access_key = AbCdEfGhIjKlMnOpQrStUvWxYz0123456789AbCd"],
    ["github.pat", "token ghp_" + "1234567890abcdefghijklmnopqrstuvwxyz"],
    ["github.oauth", "gho_" + "1234567890abcdefghijklmnopqrstuvwxyz"],
    ["github.server", "ghp_REDACTED"],
    ["github.fine_grained", "github_pat_" + "A".repeat(82)],
    ["anthropic.key", "sk-ant-" + "api03-abcdefghij1234567890XYZ"],
    ["openai.key", "sk-proj-" + "a".repeat(40)],
    ["sendgrid.key", "SG." + "a".repeat(22) + "." + "b".repeat(43)],
    ["stripe.secret", "sk_live_" + "a".repeat(30)],
    ["slack.token", "xox" + "b-1234567890-abcdefghijklmnop"],
    ["slack.webhook", "https://hooks.slack.com/services/T00000000/B11111111/" + "a".repeat(24)],
    ["discord.webhook", "https://discord.com/api/webhooks/123456789012345678/" + "a".repeat(60)],
    ["pem.private_key", "-----BEGIN RSA PRIVATE KEY-----"],
    // #1946 coverage-gap additions
    ["gitlab.token", "remote: glpat-" + "Ab12Cd34Ef56Gh78Ij90"],
    ["gitlab.token", "trigger glptt-" + "a1b2c3d4e5f6a7b8c9d0e1f2"],
    ["gitlab.token", "deploy gldt-" + "Zy98Xw76Vu54Ts32Rq10"],
    ["groq.key", "gsk_" + "AbCdEfGhIjKlMnOpQrStUvWxYz0123456789AbCdEfGhIjKlMn"],
    ["tavily.key", "tvly-" + "AbCdEfGhIjKlMnOpQrStUvWx"],
    ["tavily.key", "tvly-dev-" + "AbCdEfGhIjKlMnOpQrStUvWx"],
    ["notion.token", "ntn_" + "AbCdEfGhIjKlMnOpQrStUvWxYz0123456789AbCdEfGh"],
    ["notion.token", "secret_" + "AbCdEfGhIjKlMnOpQrStUvWxYz0123456789AbCdEfGh"],
    ["huggingface.token", "hf_" + "AbCdEfGhIjKlMnOpQrStUvWxYz012345"],
    ["npm.token", "npm_" + "a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7R8"],
    ["digitalocean.token", "dop_v1_" + "0123456789abcdef".repeat(4)],
    [
      "gcp.service_account",
      '{"private_key_id": "abc123", "private_key": "[REDACTED PRIVATE KEY]";
    expect(redactFindingSpans(msg, { repoVisibility: "private" })).toBeNull();
  });

  test("GCP service-account JSON → null (key body follows the captured marker)", () => {
    const msg =
      'config dump: {"private_key_id": "abc123", "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBg..."}';
    expect(redactFindingSpans(msg, { repoVisibility: "private" })).toBeNull();
  });

  // Pre-landing review: overlapping spans (a Bearer token that is also a
  // JWT) must coalesce — independent splices apply stale offsets and can
  // leave trailing secret bytes or mangled markers.
  test("overlapping spans (Bearer JWT fires auth.bearer + jwt) never leak and produce clean markers", () => {
    const jwt = "eyJ" + "a".repeat(20) + ".eyJ" + "b".repeat(20) + "." + "c".repeat(20);
    const out = redactFindingSpans(`Authorization: Bearer ${jwt}`, { repoVisibility: "private" });
    expect(out).not.toBeNull();
    expect(out!).not.toContain("eyJ");
    expect(out!).not.toContain("aaaa");
    expect(out!).not.toContain("cccc");
    // One coalesced, well-formed marker — no truncated fragments.
    expect(out!).toMatch(/^Authorization: Bearer <REDACTED-[a-z._+]+>$/);
  });
});

describe("taxonomy integrity", () => {
  test("every pattern has a unique id", () => {
    const set = new Set(PATTERNS.map((p) => p.id));
    expect(set.size).toBe(PATTERNS.length);
  });
  test("autoRedactable patterns have a redactToken", () => {
    for (const p of PATTERNS) {
      if (p.autoRedactable) expect(p.redactToken).toBeTruthy();
    }
  });
});
