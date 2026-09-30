# Current state — 2026-09-30

**v1 personal companion + optional local API bridge.** Working implementation, not
an autonomous enterprise service or an installed native provider app.

Implemented: three branded editions; six-skill starter packs; 12 built-in contracts;
24-slot limit and custom manifests; local rule routing/manual triage; people context;
priority/owner/due labels; source and draft review; approval revision gates; portable
backups with privacy reset; corrupt/quota/stale-tab recovery; accessible dialogs;
text-file intake; explicit provider handoff; optional server-only API adapters for
OpenAI, Anthropic, Google; bundled standalone apps and instruction ZIPs.

Local evidence: 45 Node unit/HTTP integration tests passed before release packaging.
The restricted local Chromium environment allows HTML rendering but blocks served
navigation; its memory-mode tests are not counted as persistence acceptance. The
served-origin browser suite and CI reports provide the release evidence; consult
`docs/verification.json` when present and the linked Actions run rather than assuming
an unexecuted check passed. Screenshots are generated from tested UI, not mockups.

Not verified: live paid provider responses/model quality; authenticated skill
installation in user accounts; Safari/Firefox; participant outcomes; external
security/accessibility certification. No provider entitlements or runtime spending
were added. The initial tests use HTTP/provider fixtures, explicitly labeled.

Not implemented: automatic Slack/Gmail/webhook ingestion, embeddings, native MCP UI,
cloud sync, SSO, shared team queues, immutable audit, external execution, or guaranteed
undo of provider actions. No production deployment is asserted. Next bounded work is
in `docs/NEXT-AGENT.md`; do not dilute these boundaries in marketing.
