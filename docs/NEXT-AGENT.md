# Next bounded integration slice

The companion app is working software; the native-host and automated-intake layer
is not built. Do not rebuild the shell or rename the product to hide this boundary.

First validate this release with synthetic work in a user-authorized provider
account. Install one bundled skill, deliver its included HTML, run the ordinary
handoff, and record what the host actually supports. Do not enable paid calls just
to claim integration acceptance.

For a later native MCP Apps slice, preserve the existing draft contract. Design an
authenticated state service with owner-scoped tools (list, capture, route, prepare,
submit result, inspect). Approval must be a human UI action for a specific revision,
not an LLM-callable blanket permission. Native host confirmation does not substitute
for a scoped application approval. Remote exposure, OAuth, persistence providers,
and webhook subscriptions require explicit authorization and a data retention plan.

Start intake with one read-only source selected by the user, not every inbox. Capture
source IDs/revisions, idempotency keys, timestamps, provenance and consent. Classifier
output is a proposal; ambiguous/multi-intent work still goes to triage. Event
replays must not duplicate tasks or execute twice. Do not fabricate Slack/email
connectivity, approvals, delivery receipts, or end-to-end verification.

## Copyable starting prompt

> Read AGENTS.md, STATUS.md, docs/CONTRACTS.md, docs/DECISIONS.md, and the current
> branch. Run npm run check and the served browser suite. Preserve the three themes,
> retained data, draft-only boundary, and source provenance. First demonstrate the
> smallest authorized provider-host workflow with the existing instruction bundle;
> record real host behavior separately from mocks. Propose the smallest native
> intake slice only after identifying authorized accounts and deployment boundaries.
> Do not buy services, expose the local bridge, add secrets, or call paid models
> without authorization. Fix actual failing assertions and leave revision-linked
> evidence and a clear next step.
