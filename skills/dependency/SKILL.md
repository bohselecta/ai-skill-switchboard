---
name: dependency-map
description: Find what is waiting on what.
---

# Dependency map

A provider-neutral Skill Switchboard capability. **Tasks move to this skill; the skill stays stable.**

## Use when

Use when progress depends on other work, evidence, people, or handoffs.

## Do not use when

Do not use merely because a task has an owner; use it when dependency relationships are the actual problem.

## Helpful inputs

- The work to move forward and known prerequisites or handoffs

## Output contract

A dependency brief with prerequisites, owner gaps, blocking relationships, and coordination actions.

## Instructions

Extract dependencies, prerequisite evidence, owner gaps, and next coordination actions. Do not infer a person accepted ownership.

## Effect boundary

`prepare`. No sending, spending, signing, deploying, deleting, or autonomous external actions.

This skill prepares work only. It grants no connector, tool, credential, spending, deployment, or external-action permission. Human approval applies to the exact draft revision, not to a future action.
