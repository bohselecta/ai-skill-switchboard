# Current state — 2026-09-30

**v1 personal companion + optional local API bridge.** Working implementation, not
an autonomous enterprise service or an installed native provider app.

## Delivered

Three branded editions; generated artwork and actual browser screenshots; six-skill
starter packs; 12 built-in contracts; 24-slot limit and custom manifests; local rule
routing/manual triage; people context; priority/owner/due labels; source and draft
review; approval revision gates; portable backups with privacy reset;
corrupt/quota/stale-tab recovery; keyboard-accessible dialogs; text-file intake;
explicit provider handoff; optional server-only API adapters for OpenAI, Anthropic,
Google. Each edition includes a ready-to-open app/instruction ZIP, a full README,
MIT license and provider permission grant. Downloads are reproducible with
`npm run package`; CI rejects stale committed bundles.

## Verification

[Passing release evidence](https://github.com/bohselecta/ai-skill-switchboard/actions/runs/36754358748)
checks source commit `5f4cec2aa8defd949e20d9629028f0b92ae3b532`:

- **45 Node unit and HTTP integration tests passed**, plus standalone builds.
- **22 served-browser scenario groups passed** across all three editions, including
  capture-to-approval, privacy, edits, actual persistence, downloads/restores, edition
  isolation, keyboard/mobile/reduced-motion, stale tabs, corrupt storage, quota
  failure, hostile content, and API error/retry/review gates.
- **Three app/instruction ZIPs independently validated**, including content and
  reproducibility checks. Generated assets are vendored with provenance and hashes.

Environment: GitHub-hosted Ubuntu, Node 22, Python 3.12, Playwright 1.57.0,
Chromium 143.0.7499.4; desktop 1440×1000 and mobile 390×844. Provider responses in
these tests are fixtures, not live model calls. `docs/verification.json` records
source identity and per-scenario evidence. The permanent Verify workflow checks
subsequent branch, pull-request and main revisions separately.

Local Node tests also pass. The restricted local Chromium environment permits
HTML rendering but blocks served navigation; those render-only checks are not
counted as persistence acceptance. Actual screenshots come from the served CI app,
using labeled fictional work, not generated UI mockups. Artwork is AI-generated.

## Boundaries and next step

Not verified: live provider draft quality/latency/billing; authenticated skill
installation in user accounts; Safari/Firefox; participant outcomes; independent
security/accessibility certification. No app API entitlements or live drafting
spend were added. Browser storage is local and unencrypted; export private backups.

Not implemented: automatic Slack/Gmail/webhook ingestion, embeddings, native MCP UI,
cloud sync, SSO, shared team queues, immutable audit, external execution, or guaranteed
undo of provider actions. No production deployment is asserted. The next bounded
integration slice and agent entry prompt are in `docs/NEXT-AGENT.md`; preserve these
boundaries in marketing. First use: open an edition's downloaded
`references/companion.html` and select **Explore a sample board**.
