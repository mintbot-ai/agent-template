# Publishing your fork

Once your theme looks right in `preview/index.html` and `pytest -q`
passes locally, here's how to ship it to your real Mintbot agent.

## 1. Push to GitHub

Your repo must be **public** — Mintbot pulls anonymously, no
auth required. If you're working on a private fork, make it public
before the next step.

```bash
git push origin main
```

Wait for the GitHub Actions badge on `main` to go green. If CI fails,
Mintbot will refuse the deploy with the same error.

## 2. Paste the URL into MintOffice

Open your MintOffice dashboard:

- `https://mint.mintbot.ai/` (production)
- `https://mint.mintbot.dev/` (testing)

In **Settings → Template**, paste your repo URL. Both forms work:

```
https://github.com/yourname/your-agent-skin
git@github.com:yourname/your-agent-skin.git
```

Click **Save**. Mintbot will resolve the URL, verify the repo exists
and is public, and store the reference.

## 3. Deploy

The next time your agent deploys (e.g. a fresh order, a renewal, or a
manual *Redeploy* from the Mint dashboard), Mintbot will:

1. `git pull` your repo at `main`.
2. Run the whitelist + safety tests.
3. Copy the matching files into your agent.
4. Trigger `panel_sync` so the change is live in seconds.

You can force an immediate redeploy with the **Redeploy panel** button
in MintOffice.

## 4. Iterate

Every push to `main` is a new candidate theme. Mintbot pulls on the
next deploy or panel-sync, no manual step from you. Pushes to other
branches are ignored.

## Rollback

Mintbot keeps the last known-good copy of your theme on the agent
VPS. If a push to `main` breaks CI, Mintbot won't pull it — the agent
keeps using the previous version. To recover from a bad theme that
*did* pass CI:

```bash
git revert HEAD
git push origin main
```

…and the next deploy pulls the rollback. There's no need to use the
MintOffice UI for this.

## Troubleshooting

| Symptom                                          | Cause                                        |
|--------------------------------------------------|----------------------------------------------|
| "Repo not reachable"                             | Repo is private, or URL has a typo.          |
| "CI failed on main"                              | Look at the Actions tab on GitHub.           |
| "Whitelist rejection: <path>"                    | A non-allowed file is committed. Remove it.  |
| "File size budget exceeded"                      | A CSS/JS file is too big. Trim it.           |
| Panel still looks unchanged after deploy         | Hard-refresh the panel (Ctrl+Shift+R).       |
