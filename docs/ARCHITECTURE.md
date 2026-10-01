# Architecture — tasks move, skills stay put

Skill Switchboard has four deliberately separate concepts:

1. **Task** — the durable unit of work. It owns source, context, current state, provenance,
   task journey, exact-revision approval, and export history.
2. **Skill** — a stable reusable capability contract. It describes when to use the
   capability, when not to use it, helpful inputs, expected output, preparation
   instructions, and an effect boundary.
3. **Skill station** — a skill installed in one of the board's working slots. Tasks
   queue at stations; stations do not roam the workspace or own tasks.
4. **Runner** — ChatGPT, Claude, Gemini, a local deterministic brief, or a future
   authorized model/tool that applies the current skill. A runner may change without
   changing the skill contract or task identity.

This yields the product invariant:

> **Tasks move. Skills stay put. Runners apply skills. People approve effects.**

## Routing

The v1.1 router remains intentionally small and explainable. It performs normalized,
whole-word/phrase matching against enabled stations. Exactly one matching station
routes locally. Zero or several matches go to triage. The UI names the matching
stations and phrases; it never displays an invented model-confidence percentage.

The richer skill fields (`useWhen`, `doNotUseWhen`, `requiredInputs`,
`outputContract`, `effectClass`) are contracts for people, runners, future routing
evals, and future semantic shortlisting. They are not silently interpreted as tool
permissions.

## Task journeys

An approved task may **continue to another skill**. Before moving, the current approved
stage is archived on the task with its skill identity, reviewed result excerpt,
provenance, and approval timestamp. The current result and approval are then cleared,
and the same task enters the next station in `ready` state.

A journey is not autonomous chaining:

- every stage must reach human approval before the task can continue;
- continuing does not send, spend, deploy, delete, sign, or mutate an external system;
- prior stages are context, not authority;
- correcting the original source clears the journey;
- normal rerouting changes only the current stage and does not pretend prior reviewed
  stages never happened;
- journeys are locally bounded to protect storage and prompt size.

This lets a task move through, for example, **Research lens → Decision brief → Reply
desk** without inventing one giant agent that owns the entire process.

## Capability library and board slots

The browser keeps at most 24 installed skill stations because that is a visual working
set, not a theoretical capability limit. `skills/` contains provider-neutral canonical
`SKILL.md` files generated from the same contracts used by the browser. The built-in
catalog can grow independently from what a person pins to the board.

Run `npm run skills:generate` after changing canonical skill definitions and
`npm run skills:check` to verify checked-in skill files have not drifted.

## Effect boundaries

Every skill has an `effectClass`. v1.1 built-ins and custom browser-created skills use
`prepare`: they may prepare a reviewable artifact but do not receive authority to
perform an external action. The schema reserves future classes (`read-only`,
`external-mutation`, `financial`, `destructive`) so later integrations can require
stricter gates without redefining what a skill is.

The presence of an effect class never grants that effect. External connectors,
credentials, action permissions, and application-level approvals remain separate
integration contracts.
