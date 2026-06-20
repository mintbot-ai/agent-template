/* ─────────────────────────────────────────────────────────────────────
 * theme.js — optional hooks that run after the base panel loads.
 *
 * This file is OPTIONAL — you can delete it if you only want CSS changes.
 *
 * install.sh copies it into the panel; it runs in your users' browsers, so
 * keep it small and self-contained. Avoid loading remote scripts — that's a
 * privacy and reliability dependency you now own. Guard everything behind
 * `mintbot.onReady(...)`.
 *
 * The base panel exposes a small global named `mintbot` with a few hooks.
 * The contract is intentionally tiny so it stays stable.
 * ────────────────────────────────────────────────────────────────── */

(() => {
  'use strict';

  // Wait for the panel to finish bootstrapping before we touch anything.
  if (!window.mintbot || !window.mintbot.onReady) {
    return;
  }

  window.mintbot.onReady(() => {
    // Example: change the welcome message shown above the first chat input.
    // Remove or edit as needed.
    //
    // const welcome = document.querySelector('[data-welcome]');
    // if (welcome) welcome.textContent = "Tere tulemast minu agendi juurde!";
  });
})();
