#!/usr/bin/env python3
"""
Bundle desktop/office_scene.html into desktop/plugin.js
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCENE_HTML_PATH = ROOT / "desktop" / "office_scene.html"
TEMPLATE_PATH = ROOT / "desktop" / "plugin_template.js"
OUT_PATH = ROOT / "desktop" / "plugin.js"

def main():
    scene_html = SCENE_HTML_PATH.read_text(encoding="utf-8")
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    # Serialize as JS string literal safely
    html_json = json.dumps(scene_html)
    injected = f"const SCENE_HTML = {html_json}\n"

    result = template.replace("// SCENE_HTML_PLACEHOLDER", injected)
    OUT_PATH.write_text(result, encoding="utf-8")
    print(f"[OK] Generated {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
