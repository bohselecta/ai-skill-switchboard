---
name: data-check
description: Spot the mismatch before it spreads.
---

# Data check

A provider-neutral Skill Switchboard capability. **Tasks move to this skill; the skill stays stable.**

## Use when

Use for supplied rows, totals, spreadsheet excerpts, or reconciliations that need consistency checks.

## Do not use when

Do not use when no actual data is supplied or when the task is general research.

## Helpful inputs

- The supplied data or a faithful text representation of it

## Output contract

A checkable data review with mismatches, calculation assumptions, and unresolved inputs.

## Instructions

Inspect the supplied text data for inconsistencies. Show calculation assumptions and checks. Do not fabricate rows, totals, or access to files.

## Effect boundary

`prepare`. No sending, spending, signing, deploying, deleting, or autonomous external actions.

This skill prepares work only. It grants no connector, tool, credential, spending, deployment, or external-action permission. Human approval applies to the exact draft revision, not to a future action.
