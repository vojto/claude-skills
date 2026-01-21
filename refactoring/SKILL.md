---
name: refactoring
description: Guidelines for refactoring code. Use when the user asks to refactor code.
---

## Refactoring Guidelines

- **Minimize redundant parameters**: If a value can be derived from another parameter, don't pass both. Compute it where needed to keep function signatures lean.

- **Order methods top-down**: Place caller methods before the methods they call. Entry points go first, followed by the helpers they use, so the code reads like a story from high-level to low-level.

- **Extract to shared helpers**: Move repeated patterns and pure functions (those not depending on instance state) to a dedicated helpers folder, making them reusable across the codebase.
