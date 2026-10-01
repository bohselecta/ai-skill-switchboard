# Product and engineering decisions

**2026-09-30 — v1.1: Tasks move. Skills stay put.** The task is the durable unit of
work. A skill is a stable capability contract. The visible tile is a station where
work queues, not a roaming micro-agent. Runner/provider identity is kept separate from
skill identity so ChatGPT, Claude, Gemini, or a future authorized runner can apply the
same capability without changing what the task is.

**Approved tasks can continue through another skill.** Multi-step work should not force
a mega-agent. After human approval, the same task can move to another station and
retain a bounded reviewed prior stage as context. The next stage starts unapproved.
Correcting source clears the journey. This is explicit task movement, not autonomous
chaining.

**Richer skill contracts, still a simple router.** Skills now say when to use them,
when not to use them, helpful inputs, expected output, and effect class. v1.1 still
routes using deterministic visible phrases. The added fields improve human clarity,
portable skill quality, and future evals without smuggling in a black-box classifier
or fake probability.

**24 is a board working set, not the capability ceiling.** Six starter stations remain
the default because a wall of empty tiles creates setup work. The provider-neutral
`skills/` library can grow independently. The board stays spatially stable; the
adjacent Next Decisions list prioritizes attention without moving tiles.

**Canonical skills are provider-neutral.** Built-in skill definitions generate plain
`skills/<id>/SKILL.md` files. ChatGPT, Claude, and Gemini retain distinct branded front
doors and provider wrappers, but capability semantics come from one source of truth.
CI checks the generated library for drift.

**Separate preparation from execution.** Buttons say what actually happens: copy a
request, generate a draft, approve a draft, continue a task. No simulated throughput,
fake latency, invented confidence, or success notification implying an external action.
Statuses and activity derive from real local state changes.

**Companion first; optional local API.** Copy/paste uses an existing chat account. The
optional server makes real provider API requests only after explicit consent. No OAuth,
cloud account, telemetry, database, or service subscription is needed.

**Distinct front doors; shared correctness.** Three folders own branding, artwork,
instructions, README, and permission notice. Shared vanilla modules prevent three
approval engines from drifting. Standalone HTML and skill ZIPs are build outputs.

**Local-first is not enterprise-secure.** Browser data is unencrypted, single-user,
and bounded. Public static hosting serves app code, not a cloud workspace. The local
API bridge remains loopback-only.

**Native host integration is a separate acceptance gate.** Bundled skills can prepare
results and deliver included HTML through available file tools, but they do not
silently synchronize browser state. A native integration needs state, authentication,
tool contracts, host validation, retention policy, and account testing.

**Onboarding and marketing remain honest.** Generated sculpture is labeled art;
README interface captures come from browser tests. Fictional walkthrough work is
labeled. No participant or commercial outcomes are claimed from software tests.
