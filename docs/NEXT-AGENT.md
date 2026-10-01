# Next bounded integration slice

v1.1 deliberately improves the capability model without making the interface busier.
Preserve the invariant: **Tasks move. Skills stay put. Runners apply skills. People
approve effects.** Do not replace the board with a multi-agent activity dashboard.

Before new integration work, run `npm run check` and the full served browser suite.
Confirm task-journey migration, canonical skill drift checks, three themes, retained
private data, draft-only authority, and bundle reproducibility.

## Routing evolution, when justified by evidence

The current router is deterministic and explainable. Before adding embeddings or an
LLM classifier, collect synthetic and participant-authorized routing fixtures. Evaluate
false routes, triage rate, and manual reroutes. A future semantic layer should shortlist
skills, not silently decide consequential routing. The UI should continue to show why a
route was proposed, not a fake confidence percentage.

## Native integration, later

For a native MCP Apps or equivalent slice, preserve the task and skill contracts.
Design an authenticated state service with owner-scoped tools (list, capture, route,
prepare, submit result, inspect). Approval must remain a human UI action for a specific
revision. Continuing a task to another skill is a distinct human-reviewed state change,
not permission for a runner to chain arbitrary tools.

Start automated intake with one read-only source selected by the user, not every inbox.
Capture source IDs/revisions, idempotency keys, timestamps, provenance, and consent.
Event replays must not duplicate tasks or task-journey stages.

## Copyable starting prompt

> Read AGENTS.md, STATUS.md, docs/ARCHITECTURE.md, docs/CONTRACTS.md,
> docs/DECISIONS.md, and the current branch. Run npm run check and the served browser
> suite. Preserve the three themes, retained data, draft-only boundary, source
> provenance, canonical skill library, and the invariant “Tasks move. Skills stay
> put.” Do not add a multi-agent shell. First repair any failing v1.1 acceptance or
> bundle-reproducibility checks. Only then propose the smallest authorized provider-host
> or intake slice. Do not buy services, expose the local bridge, add secrets, or call
> paid models without authorization. Leave revision-linked evidence and a clear next
> step.
