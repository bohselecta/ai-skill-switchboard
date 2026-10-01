# v1.1 acceptance gates

| Gate | Required evidence |
|---|---|
| Start without credentials | All three editions onboard into a working six-station board; empty and fictional modes are distinguished. |
| Understand the model quickly | Board and onboarding communicate “Tasks move. Skills stay put” without requiring architecture documentation. |
| Complete a useful task | Capture → route → sharing check → handoff → paste → edit → review → approve → export. No sent/executed claim. |
| Continue reviewed work | An approved task can move to a different enabled skill; prior reviewed stage stays attached; new stage starts unapproved. |
| Safe ambiguity | Multiple/no routing matches require human routing; explanations name actual matching stations/phrases rather than confidence. |
| Stable skill contracts | Built-ins and custom imports validate `useWhen`, `doNotUseWhen`, helpful inputs, output contract, effect class, instructions, and negative scope without granting tools. |
| Backward compatibility | Existing v1 skill manifests and board backups without journey fields remain readable with conservative defaults. |
| Preserve control | Source/steering/route/draft/owner changes invalidate current approval; correcting original source clears journey; stale results fail. |
| Recovery | Corrupt storage survives until explicit reset; quota failure retains old state; stale tab preserves unsaved text; invalid response remains fixable. |
| Privacy | Private tasks cannot cross the API boundary. Other tasks, people context, keys, and authority fields do not leak; only bounded prior stages from the same task may travel with it. |
| API adapter | Correct request/extraction shape for all three providers, fixed endpoints, no tools/retries, size/time limits, sanitized failures. |
| Browser quality | Desktop and mobile, keyboard focus and Escape, reduced motion, no horizontal overflow or broken art, no JS page errors. |
| Portable library | Canonical provider-neutral `skills/*/SKILL.md` files are generated from the same built-in contracts and CI rejects drift. |
| Reproducible delivery | Node checks, standalone builds, valid skill ZIPs, source/build hashes, readable provenance and license. |

`npm run check` covers pure/HTTP behavior, skill-library drift, and standalone builds.
`tests/browser.py` covers the visible journey and review flows. Full browser acceptance
uses a served Chromium origin; render-only mode is explicitly limited and does not
claim storage, downloads, or live origin behavior. Provider responses remain fixtures.

A release is not evidence of native account installation, live model quality, provider
billing behavior, enterprise integrations, or participant benefit. Those require
separate acceptance records against authorized environments.
