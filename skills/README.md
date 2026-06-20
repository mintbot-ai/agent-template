# skills/ — your own Hermes skills

Every `skills/<name>/SKILL.md` here is installed onto your agent at
`/root/.hermes/skills/<name>/SKILL.md` by `install_skill_overlay`
(`lib/common.sh`), called from both `install.sh` and `update.sh`.

This is **your layer** on top of the base skills the platform ships. The
agent loads every `SKILL.md` it finds, shows each one's `name` +
`description` in its always-present skill index, and reads the full body on
demand when the description matches what the user is asking about.

## What you can do here

- **Add a skill** the base agent doesn't have — your product docs, your
  support/returns process, a domain workflow, an API your agent should know
  how to call. Drop a new `skills/<your-skill>/SKILL.md`.
- **Override a base skill** — reuse a base skill's directory name and your
  file is copied on top after the base skills are in place, so yours wins.

## Why `product-docs/` matters for white-label

A white-label agent does **not** receive the platform's own documentation
skill (it points at the platform's docs site, which isn't yours). So out of
the box your agent doesn't know where *your* docs live. The included
[`product-docs/`](product-docs/SKILL.md) example fills that gap — edit it
with your real brand and URLs, or delete it if you have no public docs.

## SKILL.md format

```markdown
---
name: your-skill-name          # must equal the directory name, lower-kebab-case
description: "One line that says WHEN to read this skill — it's all the agent
  sees until it opens the file, so make the trigger explicit. Wrap in quotes."
version: 1.0.0
---

# A clear title

The full instructions the agent reads once the description matches. Keep it
focused on one job. Markdown, links, and fenced code blocks all work.
```

Re-running is safe: the overlay is an idempotent copy, re-applied after
every base update so your additions and overrides survive.
