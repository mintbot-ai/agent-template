# Customising your theme

Your white-label agent panel is driven almost entirely by CSS custom
properties (variables) under `:root`. Redefining a variable in
`theme/theme.css` is enough to recolour, re-shape, or re-typeface the
whole panel. Bespoke CSS rules are allowed, but try the variables
first — they age better and won't break when the panel is updated.

## Variable cheat sheet

| Variable               | What it controls                          | Default      |
|------------------------|-------------------------------------------|--------------|
| `--bg`                 | Outer page background                     | `#0b0e10`    |
| `--bg2`                | Sidebar, topbar, composer background      | `#13181b`    |
| `--bg3`                | Input fields, dropdowns                   | `#1a1f22`    |
| `--card`               | Chat bubble background (assistant)        | `#151a1d`    |
| `--accent`             | Primary brand colour                      | `#17dc94`    |
| `--accent-dim`         | Darker accent (hover, active)             | `#0fa866`    |
| `--accent-soft`        | Translucent accent (highlights, pills)    | `rgba(23,220,148,.12)` |
| `--accent-softer`      | Even softer accent (subtle backgrounds)   | `rgba(23,220,148,.06)` |
| `--text`               | Body text                                 | `#e8eaf0`    |
| `--muted`              | Secondary text                            | `#7a8690`    |
| `--muted2`             | Tertiary text (labels, section titles)    | `#545d66`    |
| `--border`             | Subtle borders                            | `#ffffff0f`  |
| `--border2`            | Slightly stronger borders                 | `#ffffff1a`  |
| `--radius`             | Card/bubble corner radius                 | `12px`       |
| `--radius-sm`          | Button/input corner radius                | `8px`        |

## Recipes

### Lavender brand

```css
:root {
  --accent:        #c89bff;
  --accent-dim:    #9d6fe0;
  --accent-soft:   rgba(200, 155, 255, .14);
  --accent-softer: rgba(200, 155, 255, .07);
}
```

### Light mode

```css
:root {
  --bg:    #fafafa;
  --bg2:   #ffffff;
  --bg3:   #f1f3f5;
  --card:  #ffffff;
  --text:  #1a1a1a;
  --muted: #6b7280;
  --border:  #e5e7eb;
  --border2: #d1d5db;
}
```

### Sharper corners

```css
:root {
  --radius:    4px;
  --radius-sm: 2px;
}
```

## Adding custom rules

If a variable doesn't cover what you want, write a CSS rule. Keep
selectors scoped to elements you can see in the preview — global
resets (`*`, `body`) can break the rest of the panel.

```css
/* Slightly larger brand wordmark */
.topbar .brand {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: .015em;
}
```

## What's NOT allowed

- `@import url("https://...")` — see `tests/test_no_external_urls.py`.
- Loading remote fonts via `@font-face` with an off-site `src`.
- CSS expressions or `@supports` selectors that fire only in dev tools.

If you need a font that isn't already loaded by the base panel, ship
it as a `data:` URI inside `theme.css`. Keep the resulting file under
the size budget in `tests/test_file_sizes.py`.

## Brand voice — two levels (`persona/`)

The visual theme above changes how the agent **looks**. To change how
the agent **talks**, the template offers two complementary files —
use one or both depending on how much you want to override.

```
┌─ mintbot baseline (always) ─────────────────┐
│ Environment header                          │  agent URL, TG bot, panel URLs
│ Capabilities                                │  tools, MEDIA marker, browser, …
├─ Persona section ───────────────────────────┤
│ persona/system_prompt.md.j2 (if present) ◄──┤  FULL brand persona — replaces
│   else: mintbot's bundled client persona    │  the bundled mintbot persona
├─ Tail overlay ──────────────────────────────┤
│ persona/brand_layer.md (if present)      ◄──┤  short voice & tone overlay
└─────────────────────────────────────────────┘
```

**`persona/system_prompt.md.j2` — full persona replacement.** The
shipped file is a working **AcmeAI** example — search-and-replace
`AcmeAI` / `Acme` for your brand name, tweak the voice section, push.
Three Jinja variables are available at render time: `{{ agent_id }}`,
`{{ panel_domain_base }}`, `{{ bot_handle }}`. Hard cap 48 KB.

**`persona/brand_layer.md` — short tail overlay.** Optional. Use this
when `system_prompt.md.j2` already carries your brand and you only
want to nudge tone with a few extra lines. Hard cap 8 KB. Keep it
small and high-signal — long persona files dilute rather than
strengthen the voice.

Both files run through the same safety contract below.

**Hard rules** (`tests/test_persona.py` enforces these — your CI will
fail if you violate them):

- No role-changing tokens: `<|system|>`, `[INST]`, `<<SYS>>`,
  `### System:`, etc. mintbot already owns the system role.
- No HTML comments (`<!-- ... -->`). The brand layer must be auditable
  in plain markdown — no hidden instructions allowed.
- No lines that start with `system:`, `user:`, or `assistant:` —
  these look like chat-completion role headers to many LLMs.
- UTF-8 plain text only. No BOM.

Inside those rules, write what you want. A typical brand layer covers
voice & tone, what your brand cares about, and a short list of things
to avoid. See the starter `persona/brand_layer.md` in the template,
and the fully worked `persona/system_prompt.md.j2` example.
