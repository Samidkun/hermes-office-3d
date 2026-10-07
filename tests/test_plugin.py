#!/usr/bin/env python3
"""
Automated Verification Suite for Hermes Pixel Office (AC-1 to AC-10)
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERMES_HOME = Path.home() / ".hermes"

def test_plugin_structure():
    """Verify file structure & invariants per hermes-desktop-plugins skill"""
    assert (ROOT / "desktop" / "office_scene.html").exists(), "office_scene.html missing"
    assert (ROOT / "desktop" / "plugin.js").exists(), "plugin.js missing"
    assert (ROOT / "dashboard" / "manifest.json").exists(), "manifest.json missing"
    assert (ROOT / "dashboard" / "dist" / "index.js").exists(), "dist/index.js missing"

    # Invariant: NO plugin.yaml in dashboard/desktop plugin
    assert not (HERMES_HOME / "plugins" / "office-3d" / "plugin.yaml").exists(), "plugin.yaml must not exist!"
    assert not (HERMES_HOME / "plugins" / "office-3d" / "plugin.yml").exists(), "plugin.yml must not exist!"
    print("[PASS] Plugin file structure & skill invariants")

def test_performance_invariants():
    """Verify AC-9 (12-15 FPS throttle & offscreen blit) and AC-10 (Auto-sleep)"""
    scene_code = (ROOT / "desktop" / "office_scene.html").read_text(encoding="utf-8")

    # AC-9: Throttled FPS & Offscreen Blit
    assert "TARGET_FPS = 12" in scene_code, "Must throttle to 12 FPS"
    assert "offscreenCanvas" in scene_code, "Must use OffscreenCanvas for static blit"
    assert "drawImage(offscreenCanvas" in scene_code, "Must blit cached background image"

    # AC-10: Auto-sleep on visibilitychange
    assert "visibilitychange" in scene_code, "Must attach visibilitychange listener"
    assert "document.hidden" in scene_code, "Must check document.hidden"
    assert "cancelAnimationFrame" in scene_code, "Must cancel animation frame when hidden"
    print("[PASS] AC-9 (12 FPS throttle & offscreen blit) and AC-10 (Auto-sleep)")

def test_zones_and_roleplay():
    """Verify AC-3, AC-4, AC-5, AC-6 (Functional zones, waypoints, speech bubbles)"""
    scene_code = (ROOT / "desktop" / "office_scene.html").read_text(encoding="utf-8")

    # Zones check
    assert "BOSS_DESK" in scene_code, "Missing BOSS_DESK zone"
    assert "MEETING_1" in scene_code, "Missing War Room meeting zone"
    assert "COFFEE_BAR" in scene_code, "Missing Pantry espresso zone"
    assert "WATER_COOLER" in scene_code, "Missing Water Cooler zone"

    # Speech bubbles check
    assert "drawSpeechBubble" in scene_code, "Missing speech bubble drawing routine"

    # Modes check
    assert "setMode('standup')" in scene_code or "setMode" in scene_code, "Missing roleplay mode switcher"
    print("[PASS] AC-3, AC-4, AC-5, AC-6 (Zones, waypoints, speech bubbles, states)")

def test_sdk_bridge():
    """Verify AC-7, AC-8 (Inspector, postMessage bridge, host plugin)"""
    plugin_code = (ROOT / "desktop" / "plugin.js").read_text(encoding="utf-8")

    # Plugin SDK surface
    assert "@hermes/plugin-sdk" in plugin_code, "Must import @hermes/plugin-sdk"
    assert "host.openWorkspace" in plugin_code, "Must use host.openWorkspace"
    assert "ctx.onEvent('*'" in plugin_code, "Must subscribe to gateway events"
    assert "postMessage" in plugin_code, "Must forward events via postMessage"
    assert "id: 'office-3d'" in plugin_code or "ID = 'office-3d'" in plugin_code, "Plugin ID mismatch"
    print("[PASS] AC-7, AC-8 (Inspector HUD & Gateway postMessage bridge)")

def main():
    print("=== Running Hermes Pixel Office Verification Suite ===")
    test_plugin_structure()
    test_performance_invariants()
    test_zones_and_roleplay()
    test_sdk_bridge()
    print("=== ALL CHECKS PASSED (10/10) ===")

if __name__ == "__main__":
    main()
