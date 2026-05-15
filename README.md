# mintbot-ai / agent-template

> Your white-label agent's look and feel — fork, customise, deploy via [MintOffice](https://mint.mintbot.ai/).

This is the **starting point** for theming a white-label agent panel.
Fork it, edit a couple of CSS variables, drop the public URL of your
fork into MintOffice, and mintbot will pull your theme onto your
agent the next time it deploys.

```
┌─ Your fork ────────────┐    ┌─ MintOffice ─────────┐    ┌─ Your agent ─────────────┐
│ github.com/me/         │ →  │  Onboarding form     │ →  │ agent123.yourdomain.com  │
│   my-agent-skin        │    │  "Template repo URL" │    │ uses your theme.css      │
└────────────────────────┘    └──────────────────────┘    └──────────────────────────┘
```

## Quick start

1. Click **Use this template** (or `git clone` then `rm -rf .git && git init`).
2. Open `theme/theme.css` and change the colours under `:root`.
3. Open `theme/theme.json` and set `name`, `author`, `description`.
4. (Optional) Open `theme/theme.js` to add tiny behavioural tweaks.
5. Open `preview/index.html` in your browser to see the result.
6. `git push` to your public GitHub repo — CI must be green.
7. Paste the repo URL into your [MintOffice](https://mint.mintbot.ai/) onboarding form.

## What you can change

| File              | Purpose | Required? |
|-------------------|---------|-----------|
| `theme/theme.css` | CSS variables + custom rules — the bulk of your theme. | Yes |
| `theme/theme.json`| Metadata (name, version, author, entry paths).         | Yes |
| `theme/theme.js`  | Small JS hooks. Leave the file empty if not needed.    | Optional |
| `preview/index.html` | Local preview of how the panel looks.               | Editable |

**Do not** add server-side code, binaries, large media files, or files
outside the whitelist — mintbot will reject the deploy. See
`tests/test_whitelist.py` for the exact allow-list.

## What runs at deploy time

When you (re)deploy your agent through MintOffice, mintbot:

1. `git pull`s your fork at `main`.
2. Runs every test in `tests/` — must pass.
3. Re-runs the whitelist check independently (defence in depth).
4. Copies the matching files into `/opt/mintbot/agent_templates/<your-agent>/web_panel/`.
5. Triggers `panel_sync` so the change is live in seconds.

If any step fails the agent keeps its previous theme — you get a
notification with the reason. Your existing setup is never broken
by a bad push to the template repo.

## Documentation

- [`docs/customizing.md`](docs/customizing.md) — every CSS variable explained.
- [`docs/publishing.md`](docs/publishing.md) — registering your fork with MintOffice.
- [`docs/reference.md`](docs/reference.md) — the JS hook surface and template contract.
- [`tests/README.md`](tests/README.md) — what each whitelist test enforces.

## Versioning

mintbot tracks your fork's `main` branch. Every push to `main` becomes
the new template for your agent at next deploy. There is no "publish"
step — `main` *is* what's live, so keep it green.

## License

MIT — see [`LICENSE`](LICENSE). You may use, modify, and ship this
template freely.
