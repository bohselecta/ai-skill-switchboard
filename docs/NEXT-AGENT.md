# Next bounded integration slice

The companion app now has the product model that future host integrations must
preserve:

**Tasks move. Skills stay put. Runners apply skills. People approve effects.**

Opening a skill is a multi-task conversation surface. It is not an agent profile.
The current companion stores the tasks, journey, questions and local approvals. It
does not yet maintain a native provider conversation or launch delegated agents.

## Next proof: one real skill session in one authorized host

First validate the existing release with synthetic work in one user-authorized
provider account.

1. Install or attach one bundled Skill Switchboard skill using an officially
   supported mechanism.
2. Open one skill session and carry two synthetic tasks through it.
3. Confirm how the host preserves conversation state, skill instructions, files,
   tool approvals and task identity.
4. Record actual host behavior separately from mocks.
5. Do not enable paid API calls merely to claim integration acceptance.

The proof should answer whether a host-native skill chat can preserve the station as
the user-facing owner while task state remains explicit and portable.

## OpenAI orchestration rule

If the host-integrated runner needs specialist execution, start with the
manager/agents-as-tools pattern documented by OpenAI. The skill session should keep
ownership of the user-facing reply while bounded agent runs help behind it.

Use a handoff only when a specialist truly needs to take over the conversation.

Delegated runs must:

- receive only the bounded context/tools required;
- return their material output/provenance to the parent task;
- never widen the skill's `effectClass`;
- never approve their own effects;
- never become new persistent board tiles by default.

Do not introduce agent identities merely to parallelize work.

## Later native state/intake slice

For a native MCP Apps or equivalent integration, preserve the existing task contract.
Design an authenticated state service with owner-scoped tools such as:

- list pinned stations and library skills;
- capture a task;
- move a task;
- inspect task/journey;
- prepare a task;
- submit a draft/result;
- answer a skill question.

Approval must remain a human UI action for a specific revision, not an LLM-callable
blanket permission. Native host confirmation does not substitute for scoped
application approval.

Start automated intake with one read-only source selected by the user, not every
inbox. Capture source IDs/revisions, idempotency keys, timestamps, provenance and
consent. Classifier output remains a proposal; ambiguous/multi-intent work still
stops in triage. Event replays must not duplicate tasks or execute twice.

Remote exposure, OAuth, persistence providers, webhook subscriptions, connector
writes, and paid provider use require explicit authorization and a retention plan.

## Copyable starting prompt

> Read AGENTS.md, STATUS.md, docs/ARCHITECTURE.md, docs/CONTRACTS.md,
> docs/DECISIONS.md, docs/ACCEPTANCE.md, and the current branch. Run npm run check
> and the served browser suite. Preserve the three themes, retained data, task
> journeys, stable skill stations, effect classes, draft-only built-ins, and source
> provenance. First demonstrate the smallest authorized host-native skill session
> with two synthetic tasks. If specialist execution is needed, keep the skill
> session user-facing and treat agent runs as bounded tools; do not turn them into
> tiles or widen permissions. Record live host behavior separately from mocks. Do
> not buy services, expose the local bridge, add secrets, or call paid models
> without authorization. Fix actual failing assertions and leave revision-linked
> evidence and a clear next step.
