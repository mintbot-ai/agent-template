/* ─────────────────────────────────────────────────────────────────────
 * theme.js — optional hooks that run after the base panel loads.
 *
 * This file is OPTIONAL — you can delete it if you only want CSS changes.
 *
 * Whitelist (enforced by tests/ and at deploy time):
 *   - No external script loading (no dynamic imports from URLs, no
 *     script-tag injection pointing off-site).
 *   - No runtime code evaluation (the eval and Function-constructor APIs
 *     are forbidden, as are dynamic import expressions).
 *   - No legacy document.write-style mutation.
 *   - File size kept under 32 KB.
 *
 * The base panel exposes a small global named `Mintbot` with a few hooks.
 * The contract is intentionally tiny so we can keep it stable.
 * ────────────────────────────────────────────────────────────────── */

(() => {
  'use strict';

  // Wait for the panel to finish bootstrapping before we touch anything.
  if (!window.Mintbot || !window.Mintbot.onReady) {
    return;
  }

  window.Mintbot.onReady(() => {
    // Example: change the welcome message shown above the first chat input.
    // Remove or edit as needed.
    //
    // const welcome = document.querySelector('[data-welcome]');
    // if (welcome) welcome.textContent = "Tere tulemast minu agendi juurde!";
  });
})();
