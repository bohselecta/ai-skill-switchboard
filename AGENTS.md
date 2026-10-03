# Working in Skill Switchboard

Read `STATUS.md`, `docs/ARCHITECTURE.md`, `docs/CONTRACTS.md`, and `docs/DECISIONS.md` before changing behavior.
The latest user request and live repository take precedence over imported proposals.

- Three editions, one safety contract. Change `shared/` once; test all three themes.
- Product invariant: tasks move; skills stay put. A skill is a capability contract and conversation surface, not an agent persona.
- The 24-tile board is the pinned working set; reusable skills may remain in the larger library.
- If a future runner delegates to agents, keep delegated runs behind the skill session, bounded by the same effect class and human approval gates.
- `npm run check`: syntax, Node unit/HTTP integration tests, static/single-file builds.
- Start `npm start`, then `npm run test:browser`. Browser test prerequisites are in `tests/requirements.txt`.
- No stubs, invented execution, fake model confidence, auto-dispatched spending, or empty controls.
- Approval is for the exact local draft revision, not a permission token for an external system.
- Private is the default. Source changes clear the draft and reset sharing. Restores never restore authority.
- No runtime dependencies or network fonts. Keep keys in the local process, never browser storage or git.
- `server.mjs` binds loopback. Do not turn it into an unauthenticated hosted proxy.
- Never call paid providers, add credentials, publish new deployments, or contact companies without authorization.
- Native instruction packs are not installed native UI integrations. Keep that distinction visible.
- Preserve state-version compatibility. A schema change needs migration fixtures and retained-data tests.
- Record the source revision and evidence kind: unit, HTTP fixture, browser, live API, or participant test.

Use `docs/NEXT-AGENT.md` for the bounded next integration slice. Keep independent repos independent.
