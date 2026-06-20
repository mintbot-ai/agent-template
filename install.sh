#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────
# install.sh — runs ONCE on your agent's VPS, after the platform has
# finished deploying and the agent is healthy. This is your hook to
# install everything client-specific: theme, brand voice, extra skills,
# seed data — anything.
#
# • Runs as root, on your own VPS. The platform's central servers never
#   run a byte of this file.
# • A failure here is logged and isolated: it can NOT break the agent or
#   block future updates. But your customization simply won't apply — so
#   keep every step idempotent and test before you push.
# • Re-running is safe by design (the runner only auto-runs install once,
#   but an operator can re-run with --force).
#
# Full environment + lifecycle: docs/contract.md
# ─────────────────────────────────────────────────────────────────────
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
. "$HERE/lib/common.sh"

log "install starting (agent=${AGENT_ID:-?}, domain=${BRAND_DOMAIN:-?})."

# 1) Panel look & feel.
install_panel_theme

# 2) Brand voice (additive overlay — the recommended persona path).
#    This MERGES persona/brand_layer.md into the agent's SOUL.md (via the
#    SOUL.local.md overlay) — your repo's contribution to the live persona.
apply_brand_voice

# 3) Your own / overriding Hermes skills (skills/<name>/SKILL.md).
#    Adds your skills to the agent's index; also fills the docs-skill gap
#    white-label agents have. See skills/product-docs/ for an example.
install_skill_overlay

# 4) Full persona replacement (advanced) — uncomment HERE and in
#    update.sh, then put your SOUL in persona/soul.full.md.
# apply_full_persona

# ── Add your own steps below ─────────────────────────────────────────
# Everything runs as root on your VPS. Use the contract env vars for
# paths. A few ideas:
#
#   • Drop in seed data / config:
#       install -D -m 0644 "$CUSTOMIZATION_DIR/data/catalog.json" \
#         "$HERMES_HOME/data/catalog.json"
#
#   • Install an OS package your tooling needs:
#       export DEBIAN_FRONTEND=noninteractive
#       apt-get update -qq && apt-get install -y -qq jq

log "install done."
