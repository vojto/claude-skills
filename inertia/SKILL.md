---
name: inertia
description: Guidelines for Rails/Inertia projects with React and Zod. Use when working with Inertia.js or Rails frontend components.
---

## Zod Schemas for Props

Use `.nullish()` instead of `.nullable()` for optional fields in Zod schemas. Rails/Inertia can return either `null` or `undefined` for missing values, and `.nullish()` handles both:

```tsx
// Good - handles both null and undefined
const PropsSchema = z.object({
  name: z.string(),
  description: z.string().nullish(),  // string | null | undefined
})

// Bad - only handles null, will fail on undefined
const PropsSchema = z.object({
  name: z.string(),
  description: z.string().nullable(),  // string | null (undefined throws)
})
```
