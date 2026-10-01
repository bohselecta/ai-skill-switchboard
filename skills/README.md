# Canonical skill library

These provider-neutral skills are the durable capability layer behind Skill Switchboard.
The board shows a small working set of **skill stations**; tasks move into those stations.
The skills themselves do not roam the workspace, own tasks, or receive tool authority.

Each folder contains a portable `SKILL.md` with the same contract used by the browser:
when to use it, when not to use it, helpful inputs, expected output, instructions, and an
effect boundary. The three ChatGPT, Claude, and Gemini editions use the same capability
semantics even though their app presentation differs.

Regenerate after changing `shared/core.mjs`:

```bash
npm run skills:generate
npm run skills:check
```

The checked-in files are deliberately plain Markdown so another host or agent can inspect,
adapt, or package them without depending on the browser app.
