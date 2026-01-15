---
name: postgres
description: Contains guides on how we use PostgreSQL. Use when you want to do something non trivial with Postgres.
---

## Stored Generated Columns

PostgreSQL generated columns are computed automatically from other columns. In Rails migrations, use `:virtual` with `stored: true`:

```ruby
add_column :orders, :total_cents, :virtual, type: :integer,
  as: "quantity * price_cents",
  stored: true
add_index :orders, :total_cents
```

The `as:` value is a PostgreSQL expression. These columns auto-update when source columns change.
