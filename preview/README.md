# Preview

Open `preview/index.html` directly in your browser to see how your
theme will look on a real white-label agent panel.

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
- `base.css` — a stripped-down copy of the base panel styles. It
  exists so you can preview without a server. **Don't edit it** — it's
  read-only here. Your changes belong in `../theme/theme.css`.

## What this preview does NOT do

- It does not run the real base panel JS — most interactions are
  inert. The point is visual feedback.
- It does not run the persona/shell checks (there is no central deploy
  gate in model A — your `install.sh`/`update.sh` run on your own VPS). Run
  `pytest -q` for the local sanity checks.
- It will look slightly different from the live panel in some details —
  the real panel has more components (file picker, modal dialogs etc.)
  that this preview deliberately doesn't include.
