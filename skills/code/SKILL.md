---
name: code-review
description: A second look before the merge.
---

# Code review

A provider-neutral Skill Switchboard capability. **Tasks move to this skill; the skill stays stable.**

## Use when

Use for source code, diffs, or pull-request changes that need review before merge.

## Do not use when

Do not use when the main need is to reproduce a known bug or create a project plan.

## Helpful inputs

- Code, diff, or pull-request context

## Output contract

A prioritized review with concrete evidence, risks, and verification steps.

## Instructions

Review supplied code for concrete correctness, security, and maintainability issues. Quote file/line evidence when present. Never claim tests ran unless logs demonstrate it.

## Effect boundary

`prepare`. No sending, spending, signing, deploying, deleting, or autonomous external actions.

This skill prepares work only. It grants no connector, tool, credential, spending, deployment, or external-action permission. Human approval applies to the exact draft revision, not to a future action.
