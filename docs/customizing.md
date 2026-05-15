# Customising your theme

The Mintbot agent panel is driven almost entirely by CSS custom
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
