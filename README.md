# agent-template

> Your white-label agent's customization repo — fork it, edit two scripts,
> point MintOffice at it, and your agent installs your customization itself.

This repo is the **starting point** for customizing a white-label agent.
You fork it, put a public GitHub URL into MintOffice, and from then on the
customization runs **on your own agent's server** — never on the platform's
central infrastructure.

```
┌─ Your fork ────────────┐    ┌─ MintOffice ─────────┐    ┌─ Your agent's VPS ───────────┐
│ github.com/me/         │ →  │  Customization repo  │ →  │ clones your repo, then runs  │
│   my-agent             │    │  URL field           │    │ install.sh (once) /          │
└────────────────────────┘    └──────────────────────┘    │ update.sh (after each update)│
                                                           └──────────────────────────────┘
```

## How it works

When your agent deploys, the platform sets up the base agent exactly as
usual, then — on **your agent's own server** — clones this repo and runs:

| Script       | Runs                                              |
|--------------|---------------------------------------------------|
| `install.sh` | **once**, after the deploy finishes and the agent is healthy |
| `update.sh`  | after **every** base-package update, once the new base is live |

The order is always **base first, your customization second** — so your
layer sits on top of a known-good agent. Your scripts run as root on your
own VPS. **The central platform never executes a byte of this repo** — it
only hands the validated URL to your server. That means you can do anything
your server can do: install OS packages, ship extra skills, replace the
persona, seed data, call your own APIs.

> Safety net: a missing, broken, or slow script is **isolated** — it can
> never break the agent or block a future update. Your customization just
> won't apply, and the reason is logged on the box. Keep your scripts
> **idempotent** and test them.

## Quick start

1. Click **Use this template** (or `git clone`, then `rm -rf .git && git init`).
2. Edit `theme/theme.css` — change the colors under `:root`.
3. Edit `persona/brand_layer.md` — your brand's voice & tone.
4. Open `preview/index.html` in your browser to check the theme.
5. (Optional) Add your own steps at the bottom of `install.sh`.
6. `git push` to a **public** GitHub repo — CI should be green.
7. Paste the repo URL into the **Customization repo** field in
   [MintOffice](https://mint.mintbot.ai/), then deploy.

## What's in here

| Path                    | Purpose                                                    |
|-------------------------|------------------------------------------------------------|
| `install.sh`            | **Required.** Your one-time post-deploy hook.              |
| `update.sh`             | Optional. Re-apply your layer after each base update.      |
| `lib/common.sh`         | Shared helpers (`install_panel_theme`, `apply_brand_voice`, …). |
| `theme/theme.css`       | Panel theme — CSS variables + custom rules.                |
| `theme/theme.js`        | Optional small JS hooks for the panel.                     |
| `persona/brand_layer.md`| Short brand-voice overlay (recommended persona path).      |
| `persona/soul.full.md`  | Optional full persona replacement (advanced).             |
| `preview/index.html`    | Local preview of your theme.                               |
| `docs/`                 | The contract, theming, persona, and publishing guides.    |
| `tests/`                | Local sanity checks (`bash -n`, shellcheck, persona rules).|

## Documentation

- [`docs/contract.md`](docs/contract.md) — the exact environment, paths, and lifecycle your scripts run under. **Start here.**
- [`docs/theming.md`](docs/theming.md) — every panel CSS variable explained.
- [`docs/persona.md`](docs/persona.md) — brand voice overlay vs. full persona replacement.
- [`docs/publishing.md`](docs/publishing.md) — registering your repo with MintOffice.

## Versioning

MintOffice tracks your repo's default branch. The agent re-clones it fresh
each time it runs `install.sh` / `update.sh`, so the latest commit is what
applies — there is no separate "publish" step. Keep your default branch
green.

## License

MIT — see [`LICENSE`](LICENSE). Use, modify, and ship freely.
