# Local checks

These run in CI (and you can run them locally) to catch mistakes before a
deploy. They are **advisory** — in the VPS-side model the platform never
runs your repo centrally, so nothing here gates a deploy. They just save you
a round-trip.

```bash
pip install pytest
pytest -q
```

`test_customization.py` checks:

| Check                              | Why                                                            |
|------------------------------------|---------------------------------------------------------------|
| `bash -n` on the three scripts     | A syntax error would abort your customization on the box.     |
| `shellcheck` (if installed)        | Catches quoting/globbing bugs that bite as root.              |
| `brand_layer.md` ≤ overlay cap     | The agent's persona CLI rejects oversize overlays at apply.   |
| No role/template markers in persona| The persona CLI rejects these — catch them here, not on deploy.|

Install `shellcheck` locally for the full set (`apt-get install shellcheck`
/ `brew install shellcheck`); without it that check is skipped.
