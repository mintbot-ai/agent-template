# Publishing your repo

Once your theme looks right in `preview/index.html` and the local checks
pass, here's how to ship it to your white-label agent via
[MintOffice](https://mint.mintbot.ai/).

## 1. Push to GitHub

Your repo must be **public** — the agent clones it anonymously, no auth
required. If you've been working on a private repo, make it public before
the next step.

```bash
git push origin main
```

Let CI go green. CI here is advisory (it runs `bash -n`, shellcheck, and the
persona safety checks) — it catches mistakes before they reach the box, but
the platform does not run your tests centrally.

## 2. Paste the URL into MintOffice

Open your MintOffice dashboard:

- [`https://mint.mintbot.ai/`](https://mint.mintbot.ai/) (production)
- [`https://mint.mintbot.dev/`](https://mint.mintbot.dev/) (testing)

In **Settings → Customization repo**, paste your repo URL:

```
https://github.com/yourname/my-agent
```

Only public `https://github.com/<owner>/<repo>` URLs are accepted (no
GitLab, self-hosted, or `git@…` SSH). Click **Save** — MintOffice validates
the URL and stores it. It does **not** clone or run anything centrally; the
URL is simply handed to your agent's server at deploy time.

## 3. Deploy

The next time your agent deploys (a fresh order, a renewal, or a manual
*Redeploy* from MintOffice), your agent's own server will:

1. Finish the standard base deploy and become healthy.
2. Clone your repo to `/opt/mintbot-agent/customization`.
3. Run `install.sh` once.

After any later base-package update, your server runs `update.sh` the same
way.

## 4. Iterate

Each run re-clones your default branch fresh, so the latest commit always
applies — there's no separate publish step. Just push and redeploy (or wait
for the next update for `update.sh` changes).

## Verifying / debugging on the box

Your scripts' output is captured on the agent's VPS:

```
/var/log/mintbot-customization.log              # stdout + stderr of every run
/var/lib/mintbot-agent/customization-state.json # commit, exit codes, fail_count
```

If something didn't apply, that log says why — a missing tool, a rejected
persona overlay, a failed copy. Because runs are fail-isolated, the agent
keeps working regardless; only your customization is affected.

## Rollback

To undo a bad customization, revert in git and redeploy:

```bash
git revert HEAD
git push origin main
```

The next run clones the reverted state. (For the panel theme specifically,
the base package re-ships a clean panel on every update, so reverting your
`theme.css` and letting `update.sh` run restores the stock look.)

## Troubleshooting

| Symptom                                   | Cause                                              |
|-------------------------------------------|----------------------------------------------------|
| URL rejected in MintOffice                | Not a public `https://github.com/owner/repo` URL.  |
| "Repo not reachable" in the log           | Repo is private, or the URL has a typo.            |
| Persona didn't change                     | Overlay rejected (size/marker) — see the log.      |
| Panel still looks unchanged after deploy  | Hard-refresh the panel (Ctrl+Shift+R).             |
| Theme reverted after an update            | Re-apply it in `update.sh` (`install_panel_theme`).|
