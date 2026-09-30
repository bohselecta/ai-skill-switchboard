# v1 acceptance gates

| Gate | Required evidence |
|---|---|
| Start without credentials | All three editions onboard into a working six-skill board; empty and fictional modes are distinguished. |
| Complete a useful task | Capture → route → sharing check → handoff → paste → edit → review → approve → export. No sent/executed claim. |
| Safe ambiguity | Multiple/no routing matches require human routing. Paused skills do not receive new automatic work. |
| Preserve control | Source/steering/route/draft/owner changes invalidate approval; stale results fail; restored approvals require review. |
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
billing, enterprise integrations, or participant benefit. Those need separate
acceptance records against authorized environments.
