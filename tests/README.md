# Template tests

These tests enforce the Mintbot **whitelist contract** — the set of rules
your fork must satisfy before Mintbot will deploy your theme onto an
agent panel. They run automatically in GitHub Actions on every push,
and Mintbot **also runs the same checks** at deploy time, so a green
CI badge is your confidence that your fork is deployable.

## What each test does

| File | Checks |
|------|--------|
| `test_whitelist.py`         | Only allowed file paths exist; required files present. |
| `test_no_external_urls.py`  | `theme.css` and `theme.js` have no off-site URLs. |
| `test_no_unsafe_js.py`      | `theme.js` does not use `eval`, `innerHTML`, dynamic `<script>` etc. |
| `test_theme_json.py`        | `theme.json` is valid, has required fields, version is semver, `entry` paths exist. |
| `test_file_sizes.py`        | Per-file size budgets are respected. |

## Running locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
pytest -q
```

You should see something like:

```
............                                                            [100%]
12 passed in 0.06s
```

## "But I want to relax a rule!"

You can't — these tests come from Mintbot, not from you. The same
checks run at deploy time, so loosening them in your fork would just
mean your CI passes but Mintbot rejects the build.

If you genuinely need a new exception (e.g. a vetted external font CDN),
open an issue at `github.com/mintbot-ai/agent-template/issues` so we
can consider raising the rule for everyone.
