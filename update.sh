#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────
# update.sh — runs after EVERY platform base-package update on your VPS,
# once the new base is live. Re-apply anything the update may have reset,
# and adjust your layer for the new base if needed.
#
# The base update ships a fresh web panel, so the theme MUST be re-copied
# here. The brand-voice overlay lives in SOUL.local.md and survives
# updates on its own — re-applying it is just self-healing.
#
# Same rules as install.sh: runs as root on your own VPS, central never
# runs it, failures are isolated, keep every step idempotent. This file
# is OPTIONAL — delete it if you have nothing to re-apply after updates.
#
# Full environment + lifecycle: docs/contract.md
# ─────────────────────────────────────────────────────────────────────
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
. "$HERE/lib/common.sh"

log "update starting (agent=${AGENT_ID:-?}, domain=${BRAND_DOMAIN:-?})."

# Re-apply the panel theme — the base update replaces the panel dir.
install_panel_theme

# Self-healing re-apply of the brand voice overlay.
apply_brand_voice

# If you use the full persona replacement, you MUST re-apply it here too:
# the base update overwrites SOUL.base.md, and this runs right after, so
# your persona wins. Uncomment in BOTH install.sh and update.sh.
# apply_full_persona

log "update done."
