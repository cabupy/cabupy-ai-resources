---
id: mobile-ux-ui
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-26
---

## Purpose

Design and review mobile UX/UI patterns for hybrid and native app contexts.

## Inputs

- Required: target platform, user flows, screen constraints.
- Optional: design system, framework choice, accessibility constraints.

## Process

1. Map primary mobile flows and interaction constraints.
2. Define navigation, feedback, and visual hierarchy.
3. Validate accessibility and performance-sensitive behaviors.

## Output Format

- UX review checklist by severity.
- UI implementation guidance with platform-specific notes.

## Guardrails

- Do not ignore touch target and readability requirements.
- Do not treat mobile layout as desktop-downscaled design.

## Quality Checks

- Critical flows are reachable with minimal friction.
- Loading, empty, and error states are explicit.

## Failure Mode

If platform details are missing, provide cross-platform mobile baseline.
