# Persona — brand voice vs. full replacement

The visual theme changes how your agent **looks**. The persona changes how
it **talks**. There are two levels — pick based on how much you want to
override.

```
┌─ base persona (always present) ─────────────┐
│ Environment, capabilities, safety, …        │  managed by the platform
├─ SOUL.local.md overlay ─────────────────────┤
│ persona/brand_layer.md  (recommended) ◄─────┤  your voice, appended on top
└─────────────────────────────────────────────┘
        ── OR, full replacement ──
┌─ SOUL.base.md (you own it entirely) ────────┐
│ persona/soul.full.md  (advanced)      ◄─────┤  replaces the whole persona
└─────────────────────────────────────────────┘
```

## Option 1 — brand voice overlay (recommended)

Edit `persona/brand_layer.md`. `install.sh` applies it via
`apply_brand_voice`, which routes through the agent's own persona CLI. That
gives you, for free:

- the same **size cap** the panel enforces (keep it short — a few KB),
- a **safety-marker check** (no chat-template / role-flip tokens), and
- an automatic **SOUL.md rebuild** + session-cache wipe so it's live at once.

The overlay is stored in `SOUL.local.md`, which **survives base updates** —
so you don't strictly need `update.sh` for it (the template re-applies it
anyway, as a self-healing no-op).

This is the right choice for almost everyone: you keep the platform's
well-tuned base persona (capabilities, safety, environment awareness) and
just add your brand's voice on top.

### Rules your overlay must follow

The persona CLI rejects an overlay that:

- exceeds the size cap, or
- contains a role/template marker (`<|system|>`, `[INST]`, `### System:`,
  HTML comments `<!-- -->`, lines starting `system:` / `user:` /
  `assistant:`, …).

If it's rejected, `install.sh` logs the reason and leaves the persona at
base — it never half-applies. The bundled `tests/` check these rules
locally so CI catches them before you deploy.

## Option 2 — full persona replacement (advanced)

Want **no platform persona at all** — your own SOUL end to end? Put it in
`persona/soul.full.md` and enable `apply_full_persona` in **both**
`install.sh` and `update.sh` (uncomment the calls).

This writes `SOUL.base.md` directly (the file the platform normally owns).
Two placeholders are substituted at apply time:

```
${AGENT_ID}        # e.g. 8061
${BRAND_DOMAIN}    # e.g. acme.example
```

### Why it must be in update.sh too

A base update overwrites `SOUL.base.md` with the platform persona. Because
the runner runs `update.sh` **right after** the update lands, calling
`apply_full_persona` there re-writes it with yours — so your persona wins
on every update, and you do **not** need to disable auto persona-updates in
the panel. If you only put it in `install.sh`, the next base update would
revert your persona until the following deploy.

A full persona is powerful but you own all of it — including keeping it
safe and capability-accurate. Most white-label brands are better served by
the overlay.
