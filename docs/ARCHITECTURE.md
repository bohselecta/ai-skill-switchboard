# Architecture — Tasks move. Skills stay put.

Skill Switchboard is intentionally **task-centric**.

A person should not have to browse a cast of AI workers and decide which synthetic
person to hire for every loose end. Work enters once. The switchboard finds the
capability that fits, moves the task to that stable skill station, and keeps the
human-visible history with the task.

> **Tasks move. Skills stay put. Runners apply skills. People approve effects.**

## The small vocabulary

### Task

The durable unit of work and the system of record.

A task owns its source, provenance, route evidence, current skill, journey, draft,
questions, revision, approval, and local owner metadata. When a task changes skills,
the task moves; its history does not reset.

### Skill

A reusable capability contract: when to use it, when not to use it, what inputs it
needs, the workflow instructions, the output contract, and its effect class.

A skill is **not** a persona, employee, agent identity, inbox account, or permission
grant. The portable contract is deliberately inspectable and versionable.

### Skill station

A skill pinned to the visible board.

The 24-tile limit applies to the working set, not the total skill library. A station
has a stable position, queue, and conversation surface. Users can learn where work
lives without tiles reordering themselves.

### Skill session / skill chat

The conversational surface opened from a skill station.

One skill chat can show several tasks at once, ask task-specific follow-up questions,
and accept a new message as a new task routed directly to that skill. The chat is a
view over durable task state rather than a second hidden task database.

The current local companion renders this experience and persists the tasks. It does
not claim a live provider conversation occurred unless a provider call or pasted
response actually exists.

### Runner

The runtime that applies a skill to a task.

In companion mode the runner may be the user's ChatGPT, Claude, or Gemini chat after
a deliberate handoff. With the optional local API bridge, the configured provider
model is the runner for one explicit draft request.

The runner is implementation infrastructure. It is not the product identity.

### Delegated run

A bounded internal execution that a runner may use to help complete part of a task.

For an OpenAI-hosted implementation, the closest orchestration fit is usually the
**manager / agents-as-tools** pattern: the skill session remains responsible for the
user-facing conversation while specialist agent runs help behind it. OpenAI
documents this distinction separately from a handoff, where another agent takes over
the conversation.

A delegated run:

- is transient execution, not another tile;
- receives only the context and tools required for its bounded job;
- cannot widen the parent skill's effect class or permission boundary;
- cannot approve its own output;
- returns evidence/results to the task and skill session;
- is surfaced as provenance or progress when that information matters to the user.

Use an actual handoff only when ownership of the user-facing conversation is
intentionally transferred. Skill Switchboard should not manufacture a cast of
agents merely to parallelize hidden work.

OpenAI references:

- Skills: https://openai.com/academy/skills/
- Agent definitions: https://developers.openai.com/api/docs/guides/agents/define-agents
- Orchestration and handoffs: https://developers.openai.com/api/docs/guides/agents/orchestration
- Running agents: https://developers.openai.com/api/docs/guides/agents/running-agents

## Relationship to Actors

An Actor in a persona/actor framework is a different abstraction.

An Actor can embody identity, perspective, continuity, preferences, and potentially
coordinate agents. A Skill Switchboard skill is intentionally narrower: a repeatable
way to perform a class of work. Do not turn skills into pseudo-people.

An Actor may use skills. An agent run may apply a skill. Neither relationship changes
what the skill is.

## Routing

Routing is a proposal, not authority.

The current local router uses explicit whole-word/phrase matches and records the
matching evidence. It does not expose invented probability scores.

Each skill contract can declare:

- `useWhen`
- `doNotUseWhen`
- `requiredInputs`
- `outputContract`
- `effectClass`
- positive/negative routing examples
- deterministic routing phrases

Exactly one local match can route automatically. Zero or several matches stop in
triage for a human choice.

A future semantic router should shortlist candidates from the same contracts, record
why they were considered, and preserve the same ambiguity stop.

## Task journeys

A task may need more than one capability.

The answer is not a mega-agent. The task moves through a sequence of bounded skills:

```text
Contract review → Decision brief → Reply desk
```

The task retains one source-of-truth record and a journey of skill transitions.
Moving a task invalidates stale draft approval and requires a fresh preparation pass
where appropriate.

## Effects and approval

Skills declare the highest kind of effect their workflow is designed to produce:

1. `read-only`
2. `draft`
3. `external-mutation`
4. `financial-commitment`
5. `destructive`

The current built-ins are draft-only.

Routing may be automatic. Preparing low-risk work may eventually be automatic.
Consequential effects remain explicit human decisions tied to an exact task revision.

Delegation never upgrades an effect class.

## Product rule

The UI should preserve one immediately understandable mental model:

- the **board** is the stable set of skill stations;
- opening a **skill** feels like chatting with that capability and its queue;
- **tasks** are the things that arrive, move, ask for judgment, and accumulate history;
- provider models and any delegated agents are runners behind the capability;
- people remain the authority for consequential effects.

That distinction is more important than exposing the internal orchestration graph.
