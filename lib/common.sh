# shellcheck shell=bash
# ─────────────────────────────────────────────────────────────────────
# lib/common.sh — shared helpers for install.sh and update.sh.
#
# Sourced by both entry scripts so the reusable "apply my customization"
# building blocks live in one place and can't drift apart. Define helpers
# here; call them from install.sh / update.sh.
#
# THE CONTRACT (set by mintbot's customization runner on YOUR OWN VPS):
#
#   PHASE              "install" | "update"
#   AGENT_ID           numeric agent id, e.g. 8061
#   BRAND_DOMAIN       your apex domain, e.g. acme.example
#   CUSTOMIZATION_DIR  this repo, checked out on the VPS (also == $PWD)
#   HERMES_HOME        the agent runtime home   (/root/.hermes)
#   MINTBOT_PANEL_DIR  the served web panel     (/opt/mintbot-agent/panel)
#
# Secrets (API tokens, BYOK keys) are deliberately NOT in the environment.
# Everything here runs as root, on your own server. The platform's central
# servers never execute a byte of this repo — see docs/contract.md.
# ─────────────────────────────────────────────────────────────────────

# Where the agent's local-api (which owns the persona CLI) is installed.
LOCALAPI_DIR="${LOCALAPI_DIR:-/opt/mintbot-agent/local-api}"

# Timestamped line to stdout. The runner captures stdout+stderr into
# /var/log/mintbot-customization.log, so anything you log is auditable.
log() { printf '[customization] %s\n' "$*"; }

# ── Panel theme ──────────────────────────────────────────────────────
# Copy your panel theme overlay into the served panel. The panel is
# served statically, so the change is live immediately — no restart.
# The base package replaces the panel directory on update, which is why
# update.sh re-runs this. Safe to call when the files don't exist.
install_panel_theme() {
  local css="$CUSTOMIZATION_DIR/theme/theme.css"
  local js="$CUSTOMIZATION_DIR/theme/theme.js"
  if [ -z "${MINTBOT_PANEL_DIR:-}" ] || [ ! -d "$MINTBOT_PANEL_DIR" ]; then
    log "panel dir not found (${MINTBOT_PANEL_DIR:-unset}) — skipping theme."
    return 0
  fi
  if [ -s "$css" ]; then
    install -D -m 0644 "$css" "$MINTBOT_PANEL_DIR/assets/css/theme.css"
    log "installed theme.css -> panel/assets/css/theme.css"
  fi
  if [ -s "$js" ]; then
    install -D -m 0644 "$js" "$MINTBOT_PANEL_DIR/assets/js/theme.js"
    log "installed theme.js -> panel/assets/js/theme.js"
  fi
}

# ── Brand voice (recommended persona path) ───────────────────────────
# Apply persona/brand_layer.md as an additive voice overlay. Routes
# through the agent's own persona CLI so the overlay gets the same size
# cap, safety-marker checks, SOUL.md rebuild and session-cache wipe the
# panel's Persona card uses. The overlay lives in SOUL.local.md, which
# SURVIVES base updates — so install.sh alone is enough; update.sh
# re-runs it only as a self-healing belt-and-braces.
apply_brand_voice() {
  local layer="$CUSTOMIZATION_DIR/persona/brand_layer.md"
  local py="$LOCALAPI_DIR/venv/bin/python3"
  if [ ! -s "$layer" ]; then
    log "no persona/brand_layer.md — leaving persona at base."
    return 0
  fi
  if [ ! -x "$py" ] || [ ! -f "$LOCALAPI_DIR/persona.py" ]; then
    log "persona CLI not found at $LOCALAPI_DIR — skipping brand voice."
    return 0
  fi
  local out
  if ! out="$(PYTHONPATH="$LOCALAPI_DIR" "$py" -m persona set-local --mode replace <"$layer" 2>&1)"; then
    log "persona CLI errored — overlay left unchanged: $out"
    return 0
  fi
  case "$out" in
    *'"ok": true'* | *'"ok":true'*) log "applied brand voice overlay -> SOUL.local.md" ;;
    *) log "persona CLI did NOT accept the overlay (too long / disallowed marker?): $out" ;;
  esac
}

# ── Extra / overridden Hermes skills (your own layer) ────────────────
# Ship the skill directories under skills/ in THIS repo into the agent's
# skill tree. Each skills/<name>/SKILL.md becomes
# $HERMES_HOME/skills/<name>/SKILL.md — Hermes rglob's that path, loads
# every SKILL.md it finds, and advertises each by its frontmatter
# `name` + `description` in the always-present skill index, opening the
# full body on demand.
#
# This is YOUR layer on top of the base skills the platform ships. Use it
# to:
#   • ADD a skill the base agent doesn't have — e.g. your own product
#     docs, your support/returns process, a domain workflow. (White-label
#     agents don't get the platform's own docs skill, so shipping your
#     product-docs skill here is the recommended way to fill that gap —
#     see skills/product-docs/ for a ready example.)
#   • OVERRIDE a base skill by reusing its directory name — your file is
#     copied on top after the base skills are in place, so yours wins.
#
# The base update re-ships the base skill tree, so this MUST also run from
# update.sh (it does) to re-apply your additions and overrides.
install_skill_overlay() {
  local src_root="$CUSTOMIZATION_DIR/skills"
  if [ ! -d "$src_root" ]; then
    log "no skills/ dir — no skill overlay to apply."
    return 0
  fi
  if [ -z "${HERMES_HOME:-}" ] || [ ! -d "$HERMES_HOME" ]; then
    log "HERMES_HOME not found (${HERMES_HOME:-unset}) — skipping skill overlay."
    return 0
  fi
  local count=0 dir name
  for dir in "$src_root"/*/; do
    [ -d "$dir" ] || continue                      # no subdirs → glob stays literal
    name="$(basename "$dir")"
    if [ ! -s "${dir}SKILL.md" ]; then
      log "skipping skill '$name' — no SKILL.md."
      continue
    fi
    install -D -m 0644 "${dir}SKILL.md" "$HERMES_HOME/skills/$name/SKILL.md"
    log "installed skill -> skills/$name/SKILL.md"
    count=$((count + 1))
  done
  log "skill overlay applied ($count skill(s))."
}

# ── Full persona replacement (advanced) ──────────────────────────────
# Replace the ENTIRE agent persona (not just an overlay) with your own
# SOUL written in persona/soul.full.md. This writes the central-managed
# SOUL.base.md directly, then rebuilds SOUL.md.
#
# The base update overwrites SOUL.base.md with the platform persona, so a
# full replacement MUST be re-applied after every update — which is
# exactly what calling this from update.sh achieves. Because the runner
# runs update.sh AFTER the base update lands, your persona wins, and you
# do NOT need to turn off auto persona-updates in the panel.
#
# NOT called by default — uncomment the calls in install.sh AND update.sh
# (both) and drop your persona into persona/soul.full.md to enable it.
# Two placeholders are substituted: ${AGENT_ID} and ${BRAND_DOMAIN}.
apply_full_persona() {
  local src="$CUSTOMIZATION_DIR/persona/soul.full.md"
  local py="$LOCALAPI_DIR/venv/bin/python3"
  if [ ! -s "$src" ]; then
    log "no persona/soul.full.md — skipping full persona."
    return 0
  fi
  if [ ! -x "$py" ] || [ ! -f "$LOCALAPI_DIR/persona.py" ]; then
    log "persona CLI not found at $LOCALAPI_DIR — skipping full persona."
    return 0
  fi
  mkdir -p "$HERMES_HOME"
  # Dependency-free placeholder substitution (no envsubst/gettext needed).
  sed -e "s|\${AGENT_ID}|${AGENT_ID:-}|g" \
      -e "s|\${BRAND_DOMAIN}|${BRAND_DOMAIN:-}|g" \
      "$src" >"$HERMES_HOME/SOUL.base.md"
  PYTHONPATH="$LOCALAPI_DIR" "$py" -m persona rebuild >/dev/null 2>&1 || true
  log "installed full persona -> SOUL.base.md (rebuilt SOUL.md)."
}
