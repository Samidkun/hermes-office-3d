# Implementation Ledger: Hermes Pixel Office

Branch: `main`
Tier: `T1`
Spec level: `spec-anchored`

## Acceptance Criteria Ledger

| Criteria ID | Status | Verify Method | Verification Evidence |
|---|---|---|---|
| `AC-1` (Mount) | PASSED | Canvas context 2D created, initial frame rendered | `office_scene.html` renders isometric tile grid & furniture on mount |
| `AC-2` (Pan/Zoom) | PASSED | Mouse drag delta updates panX/panY & wheel zoom | Event listeners on mousedown, mousemove, and wheel update camera matrix |
| `AC-3` (Waypoint Navigation) | PASSED | Character transitions gx/gy along waypoints to War Room | `setMode('standup')` animates agents along waypoints to War Room seats |
| `AC-4` (Coding State) | PASSED | Seated at workstation, typing animation, monitor scanlines | Hands animate at desk, screen glows cyan with scanline blinks |
| `AC-5` (Pantry/Break) | PASSED | Character walks to pantry, coffee mug visible | `setMode('coffee_break')` moves agents to pantry & renders red coffee mug |
| `AC-6` (Speech Bubbles) | PASSED | Comic speech bubble rendered over agent head | `drawSpeechBubble()` draws white comic balloon with dynamic message |
| `AC-7` (Inspector HUD) | PASSED | Click detection selects agent and opens HUD | Agent click raycast selects agent, updates telemetry panel & emits event |
| `AC-8` (Zero Server) | PASSED | Operates native in Hermes Desktop with zero terminal processes | Standalone ESM `desktop/plugin.js` embedded in Hermes without node server |
| `AC-9` (12 FPS Throttle) | PASSED | Frame timer limits renders to max 15 FPS, offscreen blit | `TARGET_FPS = 12` delta guard + `OffscreenCanvas` blit verified |
| `AC-10` (Auto-Sleep) | PASSED | Page visibility listener halts RAF loop when hidden | `visibilitychange` listener cancels RAF when `document.hidden === true` |

## Task Execution Waves

- [x] Task 1: Core 2.5D Isometric Engine (`office_scene.html` with Offscreen Blit, 12 FPS Throttle, Auto-Sleep)
- [x] Task 2: Character Sprite System, State Machine & Waypoint Navigation
- [x] Task 3: Interactive Inspector HUD & Speech Bubbles
- [x] Task 4: Hermes Desktop Plugin Host (`desktop/plugin.js`) & Gateway Event Bridge
- [x] Task 5: Installation Script (`scripts/install-plugin.sh`) & Documentation (`README.md`)
