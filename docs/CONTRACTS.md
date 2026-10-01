# Frozen v1.1 contract

## Product invariant

**Tasks move. Skills stay put.** A task is the durable unit of work; a skill is a
stable reusable capability. A board tile is a skill station, not a person or proof
that a model is currently running. ChatGPT, Claude, Gemini, local preparation, or a
future authorized runner may apply the skill without becoming the owner of the task.

See [ARCHITECTURE.md](ARCHITECTURE.md).

## What this product does

A personal board of 0–24 installed draft-only skill stations, starting with six. The
board captures source text, suggests a route, prepares a request, accepts a result,
records a person's local review, and can move an approved task to a subsequent skill
while retaining the reviewed prior stage as task context. Twelve built-in skills ship
in v1.1, with provider-neutral canonical `SKILL.md` files under `skills/`.

It does not grant connector permission or execute external actions. Local owner labels
add context, not notifications or verified commitments.

## State and approval invariants

`triage → ready → awaiting → review → approved` is the normal stage path. `blocked`
can return to preparation. Any open task can be closed; reopening a retained draft
requires review. Source corrections, changed direction, rerouting, draft edits, and
changed ownership invalidate current approval. Approval carries the exact task
revision and `scope: draft-only`; stale results and approvals are rejected.

An approved task may `continue` to a different enabled skill. Continuing archives the
reviewed current stage on `task.journey`, clears current result/approval/steering, and
moves the same task to the next station in `ready`. Prior stages are historical
context, not renewed authority. Correcting original source clears the entire journey.
Journeys are limited to eight completed stages, with bounded archived draft excerpts.

Every mutation uses an expected task revision. Browser writes also compare the
persisted board revision; Web Locks serialize cooperating tabs when available. A
stale tab cannot silently replace newer work. Storage remains a single-user
convenience, not a transactional distributed database.

## Routing and skill contract

`contracts/skill.schema.json` documents the portable manifest. In addition to the
existing name/description/keywords/instructions/negative scope, a skill can declare:

- `useWhen`
- `doNotUseWhen`
- `requiredInputs`
- `outputContract`
- `effectClass`

Runtime validation whitelists supported fields. Old v1 manifests without these fields
remain valid and receive conservative defaults. No manifest can add tools, scripts,
endpoints, keys, or execution rights.

Local routing normalizes whole words/phrases. Exactly one matching enabled station
routes; zero or several matches stay in triage. The route explanation names actual
matching stations/phrases. This is not embedding search, calibrated probability, or
model classification. Manual routing is explicit and visible. Pausing stops new
automatic matches, not existing work.

## Result contract

`contracts/result.schema.json`: summary ≤1,500 characters; draft 1–24,000 characters;
questions ≤10 strings of ≤500 characters. Plain text is accepted as an unverified
draft. Extra approval/execution fields are discarded. Rendered content is text, not
executable HTML or Markdown. Provider output must never approve itself.

## Privacy and interchange

Version 1 board limits: 200 tasks, 40 people, 1,000 activity entries, 12,000 source
characters/task, up to eight completed journey stages/task, and approximately 3
million serialized characters. State is scoped to edition and browser origin.
LocalStorage is not encrypted and activity history is not tamper-proof.

Exports contain private material and task journey history. They are not collaboration
links. Import validates before replacing, requires confirmation, resets all tasks to
private, returns current approved drafts to review, and never resumes API requests.
Historical journey stages remain context but do not restore current authority.
Unrecognized future versions are rejected rather than guessed or overwritten.

## API boundary

Only explicit generation sends one task, its current skill contract, steering, and
bounded prior reviewed journey stages to a fixed provider API. The payload excludes
other tasks and people context. Keys/models come from the local server environment;
no default model is assumed. The server validates Host, Origin, content type, CSRF,
request size, privacy state, contract, and one-request concurrency. It offers no
tools, auto-retries, arbitrary URL fetching, or external mutation endpoints.
Timeout/cancel stops local waiting; it does not guarantee the provider has stopped
billing. HTTP success produces a draft, never approval.

## Evidence types

`sample`: authored fictional fixture. `local`: deterministic preparation brief.
`pasted`: user-supplied result; asserted origin is not verified. `api`: returned by the
configured bridge. None establishes factual correctness or real-world outcome.
