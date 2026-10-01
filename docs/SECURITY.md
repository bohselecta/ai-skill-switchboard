# Security and privacy

Use the no-key companion with non-sensitive material first. This is a personal
product, not a regulated-data vault or a multi-user enterprise service.

The board stores source, draft, people context, and local activity in unencrypted
browser storage. Other software with access to the browser profile may read it.
Browser clearing, private sessions, quotas, or file-URL restrictions can affect
retention. Export a private backup regularly. The app warns when storage cannot be
used and preserves corrupted raw data for recovery rather than overwriting it.

Marking a task shareable records an informed local choice; it is not an employer's
permission, a legal basis, or a provider privacy guarantee. Copying a prompt to a
chat or explicitly generating through an API transmits the selected material under
that service's policies. People notes and unrelated work are excluded from model
requests. When a task has already passed through another skill, the current request
may also include bounded excerpts and summaries from those **reviewed prior task
stages** so the work can continue coherently. Those stages are context only, never
permission or approval for the current stage. Review sensitive content before
transmission; automatic redaction is not implemented and cannot be assumed.

All dynamic text is escaped. Imports whitelist IDs, URLs, dates, references, limits,
and result fields. No imported authority, executable skill manifest, prior journey stage, or source
instruction can create external-action capability. Prompt-injection resistance is
not a guarantee of model truthfulness; every result still requires human review.

The Node bridge binds only 127.0.0.1, checks Host/Origin and a per-process CSRF token,
uses fixed provider URLs, never serves .env, and sanitizes upstream errors. It has
one concurrent request and no auto-retry. Cancellation may not stop an upstream
request or its charge. Do not expose this server through a public tunnel or change
its bind address without implementing authentication and per-user authorization.

No keys are included. Do not put secrets in prompts, screenshots, backups, skill
ZIPs, bug reports, or repository issues. Report reproducible defects using synthetic
data. For a vulnerability, use GitHub private vulnerability reporting when enabled;
otherwise contact the repository owner privately without publishing exploit data.

Public static builds are UI-only; there is no hosted API bridge. This project has
not undergone a third-party penetration test, formal accessibility audit, or
compliance certification. Local activity entries are user-editable, not immutable
compliance records. Close/archive is not a deletion request at a provider.
