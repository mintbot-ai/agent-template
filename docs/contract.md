# The customization contract

This is the exact environment your `install.sh` and `update.sh` run under.
If anything here disagrees with what you observe on the box, the box wins —
please open an issue.

## Where and when your scripts run

Everything happens on **your agent's own VPS** — never on the platform's
central servers. The central side only validates your repo URL and hands it
to your server in an environment file.

```
1. Standard deploy runs and the agent becomes healthy.
2. Your server clones your repo to /opt/mintbot-agent/customization.
3. install.sh runs ONCE (over SSH, post-deploy).
   ... later ...
4. A base-package update lands and goes live.
5. update.sh runs, right after, every time.
```

The order is always **base first, your layer second**. On an update, the
new base is fully live before `update.sh` runs — so re-applying things the
base reset (the panel, a full persona) lands on top and wins.

## Environment variables

Your scripts are invoked with `bash install.sh` / `bash update.sh`, with the
repo as the working directory, and exactly this environment:

| Variable            | Example                          | Meaning                                            |
|---------------------|----------------------------------|----------------------------------------------------|
| `PHASE`             | `install` / `update`             | Which hook is running.                              |
| `AGENT_ID`          | `8061`                           | This agent's numeric id.                            |
| `BRAND_DOMAIN`      | `acme.example`                   | Your apex/brand domain.                             |
| `CUSTOMIZATION_DIR` | `/opt/mintbot-agent/customization` | This repo on disk (also `$PWD`).                 |
| `HERMES_HOME`       | `/root/.hermes`                  | Agent runtime home (SOUL, skills, state).          |
| `MINTBOT_PANEL_DIR` | `/opt/mintbot-agent/panel`       | The statically-served web panel.                   |
| `PATH`, `HOME`      | —                                | Standard root environment.                          |

**Secrets are deliberately absent.** No proxy token, no BYOK keys, no
billing credentials are placed in your script's environment. If your
customization needs a secret, fetch it yourself (e.g. from your own vault).

## Useful paths on the box

| Path                                         | What it is                                  |
|----------------------------------------------|---------------------------------------------|
| `$MINTBOT_PANEL_DIR/assets/css/theme.css`    | Panel theme CSS overlay (loaded last).      |
| `$MINTBOT_PANEL_DIR/assets/js/theme.js`      | Panel theme JS hook.                        |
| `$HERMES_HOME/SOUL.base.md`                  | Central-managed persona (overwritten on update). |
| `$HERMES_HOME/SOUL.local.md`                 | Your additive persona overlay (survives updates). |
| `$HERMES_HOME/skills/<name>/SKILL.md`        | A Hermes skill the agent indexes and reads on demand. |
| `/opt/mintbot-agent/local-api`               | The local-api install (owns the persona CLI). |
| `/var/log/mintbot-customization.log`         | Where your scripts' stdout/stderr is captured. |
| `/var/lib/mintbot-agent/customization-state.json` | Run audit: commit, exit codes, fail count. |

## Your two layers: persona and skills

Your customization sits on top of a brand-neutral base. For a white-label
agent the platform strips its own brand from the base persona and base
skills — you supply yours:

- **Persona.** `persona/brand_layer.md` is **merged into the agent's live
  `SOUL.md`**: `apply_brand_voice` feeds it through the agent's persona CLI,
  which writes `SOUL.local.md` (your additive overlay) and rebuilds
  `SOUL.md` from base + overlay. `SOUL.local.md` survives base updates, so
  `install.sh` alone is enough; `update.sh` re-applies it as a belt-and-
  braces. For a full takeover, `apply_full_persona` writes `SOUL.base.md`
  directly (and MUST run from `update.sh`, since the base update overwrites
  it). See [`persona.md`](persona.md).
- **Skills.** Every `skills/<name>/SKILL.md` in your repo is copied to
  `$HERMES_HOME/skills/<name>/SKILL.md` by `install_skill_overlay` — adding
  a new skill or, by reusing a base skill's name, overriding one. A
  white-label agent doesn't get the platform's own docs skill, so shipping
  your own `product-docs` skill is the recommended way to point the agent at
  *your* documentation. Runs from both `install.sh` and `update.sh` (the
  base update re-ships the base skill tree, so overrides must be re-applied).

## Rules of the road

- **Fail-isolated.** A missing/broken/slow script is caught and logged; it
  never breaks the agent or blocks a future update. There's a per-script
  timeout (15 min) and a clone size cap (64 MB).
- **Idempotent.** `install.sh` normally runs once, but may be re-run with
  `--force` by an operator, and `update.sh` runs on every update — so every
  step must be safe to repeat.
- **`install` runs once.** The runner records `install_done` and skips it on
  later deploys. Put recurring re-application logic in `update.sh`.
- **Log, don't guess.** Everything you print is captured. When you skip a
  step (missing tool, missing file), say so — silent no-ops are hard to
  debug from the log later.
- **You are root, on your own box.** Powerful and unsandboxed. The platform
  trusts your repo because *you* own it and it runs only on *your* server.
  Treat the repo's write access like production access.

## The repo URL rules

- Must be a **public** `https://github.com/<owner>/<repo>` URL.
- Other hosts (GitLab, self-hosted, `git@…` SSH) are refused.
- The clone is shallow (`--depth 1`) from the default branch.
