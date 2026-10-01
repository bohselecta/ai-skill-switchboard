# v1 acceptance gates

| Gate | Required evidence |
|---|---|
| Start without credentials | All three editions onboard into a working six-station board over a larger local skill library; empty and fictional modes are distinguished. |
| Understand the model | The board states that tasks move and skills stay put. Opening a skill presents a conversation with the capability and its queue, not an agent persona. |
| Use skill chat | A station can show several tasks, surface draft questions, accept a new message as a task routed directly to that skill, and preserve task state as the source of truth. |
| Complete a useful task | Capture → route/chat → sharing check → handoff → paste → edit → review → approve → export. No sent/executed claim. |
| Safe ambiguity | Multiple/no routing matches require human routing. Route evidence shows matched phrases/declared fit without a confidence percentage. Paused skills do not receive new automatic work. |
| Task journey | Moving a task to another skill appends a journey step, clears stale draft/provenance where required, and invalidates approval without duplicating the task. |
| Skill library | Up to 24 stations can be pinned while a larger library is retained. Unpinning an unused station keeps the skill available for repinning. |
| Preserve control | Source/steering/route/draft/owner changes invalidate approval; stale results fail; restored approvals require review. Effect classes do not grant action authority. |
| Recovery | Corrupt storage survives until explicit reset; quota failure retains old state; stale tab preserves unsaved text; invalid response remains fixable. |
| Privacy | Private tasks cannot cross the API boundary. Other tasks, people context, keys, and authority fields do not leak into requests. |
| API adapter | Correct request/extraction shape for all three providers, fixed endpoints, no tools/retries, size/time limits, sanitized failures. |
| Browser quality | Desktop and mobile, keyboard focus and Escape, reduced motion, no horizontal overflow or broken art, no JS page errors. |
| Reproducible delivery | Node checks, standalone builds, valid skill ZIPs, source and build hashes, readable provenance and license. |

`npm run check` covers pure/HTTP behavior. `tests/browser.py` produces an evidence
report and screenshots. Full mode uses a served Chromium origin; provider UI
responses are fixtures. Render-only mode is explicitly limited and does not claim
storage, downloads, or live origin behavior. Observed load timings are diagnostics,
not an SLA or production performance study.

A release is not evidence of native account installation, model quality, provider
billing, delegated-agent execution, enterprise integrations, or participant benefit. Those need separate
acceptance records against authorized environments.
