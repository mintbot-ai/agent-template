# Template contract reference

This document specifies the exact contract between your fork and
mintbot. If anything below contradicts the code in `tests/`, the code
wins — please file an issue so we can fix the docs.

## File layout

```
agent-template/
├── README.md             (required)
├── LICENSE               (required)
├── .gitignore            (optional)
├── .github/workflows/*.yml
├── theme/
│   ├── theme.css         (required)
│   ├── theme.js          (optional)
│   └── theme.json        (required)
├── preview/
│   ├── index.html
│   ├── base.css
│   └── README.md
├── tests/
│   ├── conftest.py
│   ├── test_whitelist.py
│   ├── test_no_external_urls.py
│   ├── test_no_unsafe_js.py
│   ├── test_theme_json.py
│   ├── test_file_sizes.py
│   └── README.md
└── docs/
    ├── customizing.md
    ├── publishing.md
    └── reference.md
```

mintbot copies **only** the `theme/` folder onto the agent VPS. Everything
else exists so that humans (you, reviewers, CI) can understand and
validate your fork. They're never served to end users.

## `theme.json` schema

```json
{
  "name":        "My Agent",               // string, 1–60 chars
  "version":     "1.0.0",                  // semver
  "author":      "Your Name",              // string
  "description": "One-line description.",  // string
  "homepage":    "https://example.com",    // optional URL
  "license":     "MIT",                    // optional SPDX id
  "preview":     "preview/index.html",     // optional, informational
  "entry": {
    "css": "theme/theme.css",              // required, must exist
    "js":  "theme/theme.js"                // optional, must exist if set
  }
}
```

## JS hook surface

The base panel exposes a global `mintbot` object. Today the surface is
intentionally tiny — we will add more hooks as patterns emerge, and
we will keep existing hooks stable.

```javascript
window.mintbot = {
  /** Register a callback to run after the panel finishes bootstrapping.
   * Callback receives no arguments. Safe to call multiple times.
   */
  onReady(callback) { /* … */ },

  /** Read-only metadata about the running agent. Available inside onReady. */
  agent: {
    name:     "string",   // the agent's display name
    template: "string",   // the template slug
    lang:     "string",   // current UI language (e.g. "en", "et")
  }
};
```

If your `theme.js` runs before the panel is ready (which it always
will, since it's loaded synchronously at the bottom of the page), you
**must** guard your initialisation by calling `mintbot.onReady(...)`.
Touching the DOM earlier will race with the panel's own setup.

## Size budgets

| Path             | Max size |
|------------------|----------|
| `theme/theme.css`| 64 KB    |
| `theme/theme.js` | 32 KB    |
| `theme/theme.json`| 8 KB    |

These limits keep agent-panel page-load fast. If you need more,
open an issue.

## Deploy-time pipeline

```
1. mintbot fetches your repo:        git clone --depth 1 <url> /tmp/agent-skin-<uuid>
2. mintbot runs your tests:          cd /tmp/agent-skin-<uuid> && pytest -q
3. mintbot re-runs the whitelist:    independent of your code, defence-in-depth
4. mintbot copies the theme/ dir:    /opt/mintbot/agent_templates/<agent>/web_panel/
5. mintbot triggers panel_sync:      pushes the new files to the agent VPS
6. mintbot deletes the clone:        rm -rf /tmp/agent-skin-<uuid>
```

If steps 2 or 3 fail, the agent keeps its previous theme and you get a
notification.

## mintbot-side validation rules (defence in depth)

Even if your local `pytest -q` passes, mintbot reapplies these checks
independently before copying anything:

- Repo URL host is `github.com` only (no other forges, for now).
- The repo is public.
- The HEAD of `main` is reachable.
- The whitelist in `tests/test_whitelist.py` matches mintbot's own.
- No file exceeds the size budget.
- `theme/` is the only directory whose contents are deployed.

We will publish the full validator code as part of the mintbot
`mintbot.ai` repo so you can audit it.
