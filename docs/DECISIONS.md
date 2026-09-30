# Product and engineering decisions

**2026-09-30 — v1 contract.** Preserve the original control-board idea, but make the
unit of value a prepared decision rather than an autonomous micro-agent. A tile is
a contract and queue; it is not a person or evidence that a model is running.

**Start with six; grow to 24.** A wall of empty tiles creates setup work. Three
starter packs are useful immediately. Spatial tile order stays stable; the adjacent
Next Decisions list prioritizes high-attention work without moving targets.

**Separate preparation from execution.** Buttons say what actually happens: copy a
request, generate a draft, approve a draft. No simulated throughput, fake latency,
invented confidence, or success notification implying an email was sent. Statuses
and activity derive from real local state changes.

**Companion first; optional local API.** Copy/paste uses an existing chat account.
The optional server makes real provider API requests only after explicit consent.
This avoids a subscription trap and makes no claims about account entitlements.
No OAuth, cloud account, telemetry, database, or service subscription is needed.

**Distinct front doors; shared correctness.** Three folders own branding, artwork,
instructions, README, and permission notice. Shared vanilla modules prevent three
approval engines from drifting. Standalone HTML and skill ZIPs are build outputs;
source stays readable and testable. This is not three independent repositories.

**Local-first is not enterprise-secure.** Browser data is unencrypted, single-user,
and bounded. Public static hosting serves app code, not a cloud workspace. The
local API bridge is deliberately not a serverless public endpoint.

**Native host integration is a separate acceptance gate.** The bundled skill can
prepare results and deliver the included HTML through available file tools, but it
cannot silently synchronize the browser. A proper MCP Apps integration requires a
state service, authentication, tool contracts, host validation, and account testing.
Do not represent a README architecture diagram as an installed integration.

**Onboarding and marketing remain honest.** Generated sculpture is labeled art;
README interface captures come from browser tests. Fictional walkthrough work is
labeled in tiles, drawers, and provenance. No participant or commercial outcomes
are claimed from software tests.
