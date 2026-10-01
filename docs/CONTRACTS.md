# Frozen v1.1 contract

## Product invariant

**Tasks move. Skills stay put. Runners apply skills. People approve effects.**

The durable object is the task. A skill is a reusable capability contract. A skill
pinned to the visible board is a station. Opening a station shows a skill chat: a
conversation surface over that skill's task queue, not a new autonomous identity.

See `docs/ARCHITECTURE.md` for the vocabulary and the OpenAI runner/delegation
mapping.

## What this product does

A personal board starts with six pinned skill stations and supports up to 24 visible
stations. The library can hold a larger set of skills. A task can be captured through
general intake or sent directly to a skill chat.

The board captures source text, records route evidence, prepares a request, accepts a
result, records task questions and a person's local review, and preserves the task's
journey if it moves between skills.

It does not grant connector permission or execute external actions. Local owner labels
add context, not notifications or verified commitments.

## Task, station, and skill-chat invariants

A task owns its source, current skill, route evidence, journey, draft, questions,
revision, approval and provenance.

A skill chat may:

- show multiple tasks currently in that skill;
- accept a new message as a new task routed directly to the skill;
- surface task-specific questions returned by a draft;
- accept an answer as new steering that requires a fresh preparation pass.

The skill chat is not a second source of truth. Answers and new work become task state.

A station's visual position stays stable. Prioritization happens in the adjacent
decision queue rather than by moving tiles around.

The 24-slot board is the working set, not the total capability ceiling. Unpinning an
unused station keeps its skill in the library.

## State and approval invariants

`triage → ready → awaiting → review → approved` is the normal path. `blocked` can
return to preparation. Any open task can be closed; reopening a retained draft
requires review.

Source corrections, changed direction, movement to another skill, draft edits, and
changed ownership invalidate approval. Approval carries the task revision and
`scope: draft-only`; stale results and approvals are rejected. A retained result
must be in review, approved, or closed state. Closing is not external completion.

Every mutation uses an expected task revision when modifying a task. Browser writes
also compare the persisted board revision; Web Locks serialize cooperating tabs when
available. A stale tab cannot silently replace newer work.

The additive v1.1 state still accepts earlier v1 backups that do not contain
`library`, richer skill fields, route evidence, or task journeys. Validation
reconstructs safe defaults rather than discarding work.

## Routing and skill contract

`contracts/skill.schema.json` documents the portable manifest.

Runtime validation whitelists supported fields. No manifest can add scripts,
endpoints, credentials, tools, or execution rights.

A skill can declare:

- `useWhen`
- `doNotUseWhen`
- `requiredInputs`
- `outputContract`
- `effectClass`
- positive/negative routing examples
- deterministic routing phrases
- instructions and negative scope

Local routing normalizes whole words/phrases. Exactly one matching enabled station
routes automatically; zero or several matches stay in triage. The route records the
matching phrases and the skill's declared fit as evidence.

This is not embedding search, calibrated probability, or model classification.
Manual routing is explicit and visible. Pausing stops new automatic matches, not
existing work.

## Task journeys

A task can move between bounded skills instead of being handed to a mega-agent.

Each move appends a journey step with the destination skill, time, and reason. The
current skill must be pinned; historical journey steps may reference skills that
remain only in the library.

Moving a task clears stale draft/provenance state and invalidates approval.

## Effect classes

Skills declare the highest intended effect class:

1. `read-only`
2. `draft`
3. `external-mutation`
4. `financial-commitment`
5. `destructive`

Current built-ins are draft-only. An effect class describes the workflow boundary; it
does not itself grant permission. Consequential actions require a separate explicit
human-approved action surface in any future integration.

## Runner and delegation boundary

A skill is not an agent. The runner is the runtime applying the skill to a task.

In this release, the runner is either a user's provider chat after explicit handoff
or the configured local API model for one explicit generation request.

This release does **not** spawn delegated agents.

A future host-integrated runner may use bounded agent runs as tools behind a skill.
Those runs must not widen the parent skill's effect class, acquire new permissions,
approve their own work, or become separate user-facing identities by default. Their
material results/provenance return to the parent task.

## Result contract

`contracts/result.schema.json`: summary ≤1,500 characters; draft 1–24,000 characters;
questions ≤10 strings of ≤500 characters. Plain text is also accepted as an
unverified draft. Extra approval/execution fields are discarded. Rendered content is
text, not executable HTML or Markdown.

Provider output must never approve itself. A question surfaced in skill chat does not
change task authority. Answering it becomes steering and requires a fresh result.

## Privacy and interchange

Board limits: 24 pinned stations, 120 library skills, 200 tasks, 40 people, 1,000
activity entries, 12,000 source characters/task, and approximately 3 million
serialized characters.

State is scoped to edition and browser origin. LocalStorage is not encrypted and
activity history is not tamper-proof. Exports contain private material. They are not
collaboration links.

Import validates before replacing, requires confirmation, resets all tasks to
private, and returns approved drafts to review. It never resumes API requests.
Unrecognized future state versions are rejected rather than guessed or overwritten.

## API boundary

Only explicit generation sends one task plus its contract to a fixed provider API.
The payload excludes other tasks, skill-chat siblings, people context and library
metadata.

Keys/models come from the local server environment; no default model is assumed. The
server validates Host, Origin, content type, CSRF, request size, privacy state,
contract, and one-request concurrency. It offers no tools, auto-retries, arbitrary
URL fetching, delegated agents, or external mutation endpoints.

Timeout/cancel stop local waiting; they do not guarantee the provider has stopped
billing. HTTP success produces a draft, never approval.

## Evidence types

`sample`: authored fictional fixture.  
`local`: deterministic preparation brief.  
`pasted`: user-supplied result; asserted origin is not verified.  
`api`: returned by the configured bridge.

None establishes factual correctness, delegated-agent execution, or a real-world
outcome.
