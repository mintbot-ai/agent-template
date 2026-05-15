# Preview

Open `preview/index.html` directly in your browser to see how your
theme will look on a real Mintbot agent panel.

```bash
# macOS
open preview/index.html

# Linux
xdg-open preview/index.html

# Or just double-click the file in your file manager.
```

## What's in this folder

- `index.html` — a self-contained mock of the panel UI (topbar, sidebar,
  chat stream, composer). It loads `base.css` first, then your
  `../theme/theme.css` on top.
- `base.css` — a stripped-down copy of Mintbot's base panel styles. It
  exists so you can preview without a server. **Don't edit it** — it's
  read-only here. Your changes belong in `../theme/theme.css`.

## What this preview does NOT do

- It does not run the real Mintbot panel JS — most interactions are
  inert. The point is visual feedback.
- It does not validate the whitelist or any other deploy gate. Run
  `pytest -q` for that.
- It will look slightly different from the live panel in some details —
  the real panel has more components (file picker, modal dialogs etc.)
  that this preview deliberately doesn't include.
