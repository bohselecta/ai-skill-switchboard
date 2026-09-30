# Frozen v1 contract

## What this product does

A personal board of 0–24 draft-only skill contracts, starting with six. The board
captures source text, suggests a route, prepares a request, accepts a result, and
records a person's local review. It does not grant connector permission or execute
external actions. Twelve built-in skills cover three starter packs. Local owner
labels add context, not notifications or verified commitments.

## State and approval invariants

`triage → ready → awaiting → review → approved` is the normal path. `blocked` can
return to preparation. Any open task can be closed; reopening a retained draft
requires review. Source corrections, changed direction, rerouting, draft edits,
and changed ownership invalidate approval. Approval carries the task revision and
`scope: draft-only`; stale results and approvals are rejected. A retained result
must be in review, approved, or closed state. Closing is not external completion.

Every mutation uses an expected task revision when modifying a task. Browser writes
also compare the persisted board revision; Web Locks serialize cooperating tabs
when available. A stale tab cannot silently replace newer work. Storage remains a
single-user convenience, not a transactional distributed database.

## Routing and skill contract

`contracts/skill.schema.json` documents the portable manifest. Runtime validation
whitelists supported fields. No manifest can add tools, scripts, endpoints, keys,
or execution rights. Local routing normalizes whole words/phrases: exactly one
matching enabled skill routes; zero or several matches stay in triage. This is not
embedding search, calibrated probability, or model classification. Manual routing
is explicit and visible. Pausing stops new automatic matches, not existing work.

## Result contract

`contracts/result.schema.json`: summary ≤1,500 characters; draft 1–24,000 characters;
questions ≤10 strings of ≤500 characters. Plain text is also accepted as an
unverified draft. Extra approval/execution fields are discarded. Rendered content
is text, not executable HTML or Markdown. Provider output must never approve itself.
The fixtures demonstrate an ordinary result and malicious extra authority fields.

## Privacy and interchange

Version 1 board limits: 200 tasks, 40 people, 1,000 activity entries, 12,000 source
characters/task, and approximately 3 million serialized characters. State is scoped
to edition and browser origin. LocalStorage is not encrypted and activity history
is not tamper-proof. Exports contain private material. They are not collaboration
links. Import validates before replacing, requires confirmation, resets all tasks
to private, and returns approved drafts to review. It never resumes API requests.
Unrecognized future versions are rejected rather than guessed or overwritten.

## API boundary

Only explicit generation sends one task plus its contract to a fixed provider API.
The payload excludes other tasks and people context. Keys/models come from the
local server environment; no default model is assumed. The server validates Host,
Origin, content type, CSRF, request size, privacy state, contract, and one-request
concurrency. It offers no tools, auto-retries, arbitrary URL fetching, or external
mutation endpoints. Timeouts/cancel stop local waiting; they do not guarantee the
provider has stopped billing. HTTP success produces a draft, never approval.

## Evidence types

`sample`: authored fictional fixture. `local`: deterministic preparation brief.
`pasted`: user-supplied result; asserted origin is not verified. `api`: returned by
the configured bridge. None establishes factual correctness or real-world outcome.
