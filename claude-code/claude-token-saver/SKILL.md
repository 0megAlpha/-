---
name: claude-token-saver
description: Use when the user mentions Claude Code token usage, prompt cache hit rate, TTL/expiry, the 1M context window, cache misses, output spikes, rate-limit caps (5h/7d), or anything in the statusline produced by claude-token-saver (chips like "🚨 5H 94%", "🚨 7D 92%", "⚠ 1M ON", "⚠ Input spike", "⚠ Cache miss", "⚠ 5m TTL", "⚠ Rebuild churn", "⚠ Output heavy", "⚠ Call surge", "⏳ Cache expires", "💰 Cache saved", "🧠 Cache hit"). Also use when they ask to view token-usage history, want to understand a warning they just saw, or want to back up work before a session cap with `claude-token-saver handoff`.
---

# claude-token-saver — Claude Code Token Monitor

This skill helps users interpret and act on the `claude-token-saver` statusline
in Claude Code. The statusline updates every ~1s and shows cache health, TTL
countdown, savings, and (when relevant) a leading warning chip.

## Response language

Respond in the user's configured output language. Run
`claude-token-saver mode` once at the start of the session and read the
`Output language` field — if it shows `language: ko`, write **all of your
prose to the user in Korean** (summary, "All clear" status lines, headings,
recommendations). If it shows `language: en` (the default), write in
English. Tool output (the body of `last`/`history`/the table report) is
already localized by the CLI — do not retranslate it; just mirror your
own narration to match. If the user asks for a different language inline,
honor that for the rest of the turn without changing the saved setting.

## When this skill should activate

- The user references any chip wording: `🚨 5H NN%`, `🚨 7D NN%`,
  `⚠ 1M ON`, `⚠ Input spike`, `⚠ Cache miss`, `⚠ 5m TTL`,
  `⚠ Rebuild churn`, `⚠ Output heavy`, `⚠ Call surge`.
- The user asks "why is my cache hit rate low", "what does this warning mean",
  "when did this start happening", or similar.
- The user is approaching a rate-limit cap and wants to back up the current
  work so a fresh session can continue (point them at
  `claude-token-saver handoff`).
- The user wants to see the token-usage history file or asks for a summary
  of recent warnings.
- The user asks for a quick token report or "current state" check (the
  skill replaces the legacy `/token-monitor` slash command — same workflow,
  triggered by intent rather than a typed slash).

## What to do

1. **Lead with the most recent warning + how to handle it.** Run
   `claude-token-saver last` first. It returns the most recent warning event
   (chip + detail + timestamp) plus the full advice block for it. Surface that
   to the user before anything else — this is what they came for.
2. **Identify the chip.** If the user pasted a statusline (instead of relying
   on `last`), pull out the leading `⚠ ...` chip. That maps to a specific
   issue category.
3. **Show recent history.** Run `claude-token-saver history` (default last 7
   days) to see the chronology of warning transitions. Each entry is timestamped,
   bilingual (English line + 한국어), and includes a `💡` action tip inline.
4. **Drill down on the live state.** Run `claude-token-saver --days 1` (or
   another window) to render the full table view, which lists per-session
   spikes and recommended actions.
5. **Explain the warning** in plain language. Use the chip → cause table:

   | Chip               | Likely cause                                          |
   | ------------------ | ----------------------------------------------------- |
   | `🚨 5H NN%`       | 5-hour rate-limit window at NN% (>=90%). Cap is imminent. |
   | `🚨 7D NN%`       | 7-day rate-limit window at NN% (>=90%). Pace yourself.   |
   | `⚠ 1M ON`         | Auto-promoted to 1M context (Opus 4.7+ Max default).  |
   | `⚠ Input spike`   | One request consumed >250k or >3× the recent p95.     |
   | `⚠ Cache miss`    | Cache hit rate dropped below ~70%.                    |
   | `⚠ 5m TTL`        | Most cache writes are 5-min ephemeral (Pro plan default). |
   | `⚠ Rebuild churn` | Cache being re-written rapidly — prefix is unstable.  |
   | `⚠ Output heavy`  | Output ratio dominates input — inspect long generations. |
   | `⚠ Call surge`    | Request count is well above baseline.                 |

6. **Suggest the next action.** For `🚨 5H/7D` chips, recommend running
   `claude-token-saver handoff` to back up the current work to a
   `HANDOFF-*.md` file before the cap hits, then continue in a fresh
   session. For 1M ON, mention `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. For
   5m TTL, point at the Max plan's 1h bucket. For input spike, suggest
   splitting the conversation or compacting context.

## Useful commands

- `claude-token-saver last` — most recent warning + full advice (start here).
- `claude-token-saver last --days 7` — widen the lookback window.
- `claude-token-saver` — full table report (default last 1 day).
- `claude-token-saver --days 7` — wider window.
- `claude-token-saver history` — recent warning transitions per day, with
  inline `💡` action tips.
- `claude-token-saver history --days 30` — longer history.
- `claude-token-saver handoff` — write a HANDOFF-*.md template in cwd
  capturing git status + cap snapshot, so a fresh session can resume cleanly.
- `claude-token-saver mode` — show statusline preferences.
- `claude-token-saver mode icon verbose 1d` — change preferences.

## Storage layout (for reference)

History files live under the OS-appropriate user-data dir:
- Windows: `%APPDATA%\claude-token-saver\history\YYYY-MM-DD.md`
- macOS:   `~/Library/Application Support/claude-token-saver/history/YYYY-MM-DD.md`
- Linux:   `~/.config/claude-token-saver/history/YYYY-MM-DD.md`

Each day's file is plain Markdown — safe to open in any editor.
