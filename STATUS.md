# Current state — 2026-09-30

**v1.1 task-to-skill companion + optional local API bridge.** Working implementation,
not an autonomous enterprise service or installed native provider app.

## Product model

The visible invariant is now explicit: **Tasks move. Skills stay put.** A task carries
its source, current station, review state, approval, and bounded journey. A skill is a
stable capability contract. The provider/model is a runner, not the skill and not the
task owner.

## Delivered

Three branded editions; generated artwork and actual browser screenshots; six-skill
starter packs; 12 built-in contracts; 24 board working slots and custom manifests;
provider-neutral canonical `skills/*/SKILL.md` library; deterministic explainable local
routing/manual triage; richer Use when / Do not use / input / output / effect contracts;
people context; priority/owner/due labels; source/draft review; exact-revision approval;
approved task journeys between skills; portable backups with privacy reset; corrupt,
quota, and stale-tab recovery; keyboard-accessible dialogs; text-file intake; explicit
provider handoff; optional server-only API adapters for OpenAI, Anthropic, and Google.

A task journey archives a bounded approved prior stage before moving the same task to
another enabled skill. It is not autonomous chaining and grants no external authority.
Correcting original source clears the journey.

## Local verification while developing v1.1

- **51 Node unit and HTTP integration tests passed** locally.
- **18 render-only Chromium scenario groups passed** across the three editions,
  including the new approved-task journey, routing explanation, custom-skill flow,
  keyboard focus, reduced motion, and mobile layout.
- Static builds for all three standalone editions succeeded.
- `npm run skills:check` confirms the 12 checked-in canonical skills match the source
  contracts.

The local environment blocks served localhost navigation in Chromium, so persistence,
download/restore, stale-tab, storage-failure, and API UI acceptance still require the
GitHub-hosted served-browser workflow before this branch is release-ready. Do not turn
render-only results into a served-origin claim.

## Existing verified v1 evidence

The previous v1 release was verified in GitHub-hosted Ubuntu with 45 Node/HTTP tests
and 22 served-browser scenario groups. v1.1 changes routing explanations, skill
contracts, task state, UI, generated skill files, and bundles; it therefore requires a
fresh CI result rather than inheriting the old release's acceptance.

## Boundaries and next step

Still not implemented: automatic Slack/Gmail/webhook intake, embedding/semantic
routing, native synchronized host UI, cloud sync, SSO, shared team queues, immutable
audit, or external execution. No production deployment is asserted.

Next: run the full GitHub Actions acceptance suite against the v1.1 review branch,
refresh reproducible edition ZIPs, inspect browser evidence, and only then consider a
merge. Native intake remains a later separately authorized slice.
