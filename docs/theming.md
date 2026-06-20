# Theming the panel

Your agent panel is driven almost entirely by CSS custom properties
(variables) under `:root`. `install.sh` copies `theme/theme.css` into the
panel as the **last** stylesheet, so any variable you redefine wins.
Redefining variables is enough to recolor, re-shape, or re-typeface the
whole panel. Bespoke CSS rules are allowed too — but try the variables
first; they age better across panel updates.

Open `preview/index.html` in a browser to see your changes locally before
you push.

## Variable cheat sheet

| Variable           | What it controls                       | Default      |
|--------------------|----------------------------------------|--------------|
| `--bg`             | Outer page background                  | `#0b0e10`    |
| `--bg2`            | Sidebar, topbar, composer background   | `#13181b`    |
| `--bg3`            | Input fields, dropdowns                | `#1a1f22`    |
| `--card`           | Chat bubble background (assistant)     | `#151a1d`    |
| `--accent`         | Primary brand color                    | `#17dc94`    |
| `--accent-dim`     | Darker accent (hover, active)          | `#0fa866`    |
| `--accent-soft`    | Translucent accent (highlights, pills) | `rgba(23,220,148,.12)` |
| `--accent-softer`  | Even softer accent (subtle backgrounds)| `rgba(23,220,148,.06)` |
| `--text`           | Body text                              | `#e8eaf0`    |
| `--muted`          | Secondary text                         | `#7a8690`    |
| `--muted2`         | Tertiary text (labels, section titles) | `#545d66`    |
| `--border`         | Subtle borders                         | `#ffffff0f`  |
| `--border2`        | Slightly stronger borders              | `#ffffff1a`  |
| `--radius`         | Card/bubble corner radius              | `12px`       |
| `--radius-sm`      | Button/input corner radius             | `8px`        |

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

## Custom rules

If a variable doesn't cover what you want, write a CSS rule. Keep selectors
scoped to elements you can see in the preview — global resets (`*`, `body`)
can break the rest of the panel.

```css
/* Slightly larger brand wordmark */
.topbar .brand {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: .015em;
}
```

## Fonts and assets

The theme is copied to your own server, so external `@import` / `@font-face`
URLs are not blocked the way they were under the old central model — but
remember **everything loads in your users' browsers**. Prefer self-hosting
fonts (ship them via your own steps in `install.sh`) or embed a small font
as a `data:` URI in `theme.css`. Third-party URLs are a privacy and
reliability dependency you own.

## JS hooks (optional)

`theme/theme.js` runs after the panel finishes bootstrapping. Guard your
code with `mintbot.onReady(...)` — touching the DOM earlier races with the
panel's own setup. The hook surface is intentionally tiny and stable:

```javascript
window.mintbot.onReady(() => {
  // mintbot.agent.name / .template / .lang are available here.
});
```
