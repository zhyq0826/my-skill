---
name: code-simplifier
description: Code simplification for clarity, consistency, and maintainability while preserving exact behavior. Use when simplifying code, reducing complexity, cleaning up recent changes, applying refactoring patterns, or improving readability. Triggers on code cleanup, simplification, refactoring, or readability improvements.
---

# Code Simplifier

Comprehensive code simplification guide. Preserve exact behavior; change how code is written, never what it does.

## When to Apply

- Simplifying or cleaning up recently modified code
- Reducing nesting, complexity, or duplication
- Improving naming and readability
- Applying language-specific idiomatic patterns
- Reviewing code for maintainability issues

## Core Principles

1. **Clarity Over Brevity**: Explicit, readable code beats clever one-liners.
2. **Scope Discipline**: Focus on recently modified code; keep diffs small.
3. **Behavior Preservation**: Change how code is written, never what it does. All outputs, errors, and side effects must remain identical.
4. **Context First**: Understand project conventions (CLAUDE.md, lint config, existing patterns) before making any changes.

## Rule Categories (by priority)

### 1. Context Discovery (CRITICAL)

- Project conventions override generic best practices.
- Match existing code style in the file and project.
- Check for linting/formatting configs (ESLint, Prettier, etc.).
- Read CLAUDE.md (or equivalent) before simplifying.

### 2. Behavior Preservation (CRITICAL)

- Verify behavior preservation before finalizing (run tests, spot-check).
- No subtle semantic changes (e.g. truthiness, order of evaluation).
- Preserve side effects: logging, I/O, state changes.
- Preserve public function signatures and types.
- Preserve error messages, types, and handling.
- Preserve all return values and outputs.

### 3. Scope Management (HIGH)

- Respect module and component boundaries.
- Avoid global rewrites and architectural changes.
- No unrelated refactors; only what was asked.
- Keep changes small and reviewable (minimal diff).
- Focus on recently modified code unless the user asks to expand.

### 4. Control Flow (HIGH)

- Simplify boolean expressions; prefer positive conditions over double negatives.
- Use optional chaining and nullish coalescing where appropriate.
- Flatten deep nesting (max 2–3 levels); use guard clauses and early returns.
- Prefer explicit control flow over dense expressions; avoid nested ternaries.
- Each block should have a single responsibility.

### 5. Naming and Clarity (MEDIUM–HIGH)

- Use intention-revealing names; avoid generic names and cryptic abbreviations.
- Use nouns for data, verbs for actions; consistent vocabulary.
- Prefer string interpolation over concatenation where clearer.

### 6. Duplication (MEDIUM)

- Prefer data-driven patterns over repetitive conditionals when it improves clarity.
- Prefer duplication over premature abstraction (rule of three).
- Extract only when it improves clarity; avoid single-use helpers.

### 7. Dead Code (MEDIUM)

- Remove stale TODO/FIXME comments; keep comments that explain *why*, not *what*.
- Remove obvious comments; delete unused code, never comment it out.

### 8. Language Idioms (LOW–MEDIUM)

- Prefer language and stdlib builtins.
- Go: handle errors immediately.
- Python: use comprehensions for simple transforms.
- TypeScript: use strict types over `any`, const assertions and readonly where appropriate.

## Workflow

1. **Discover context**: Read CLAUDE.md, lint configs, examine existing patterns.
2. **Identify scope**: Focus on recently modified code unless asked to expand.
3. **Apply in order**: Use rules in priority order (CRITICAL first).
4. **Keep diffs minimal**: Small, focused changes that are easy to review.
5. **Verify behavior**: Ensure outputs, errors, and side effects remain identical.

## Balance

Avoid over-simplification that:

- Reduces readability or creates overly clever solutions
- Removes helpful abstractions
- Makes code harder to debug

When in doubt, prefer clarity and minimal, reviewable changes.
