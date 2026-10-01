---
name: bug-brief
description: Make the failure reproducible.
---

# Bug brief

A provider-neutral Skill Switchboard capability. **Tasks move to this skill; the skill stays stable.**

## Use when

Use for a software failure, regression, or defect that needs a reproducible report.

## Do not use when

Do not use for a general code review without an observed failure.

## Helpful inputs

- Observed failure and any known environment, reproduction steps, logs, or screenshots

## Output contract

A reproducible bug brief with observed/expected behavior, evidence, missing details, and untested hypotheses.

## Instructions

Produce a reproducible bug report: environment, steps, observed and expected behavior, available evidence, missing details. Label untested hypotheses.

## Effect boundary

`prepare`. No sending, spending, signing, deploying, deleting, or autonomous external actions.

This skill prepares work only. It grants no connector, tool, credential, spending, deployment, or external-action permission. Human approval applies to the exact draft revision, not to a future action.
