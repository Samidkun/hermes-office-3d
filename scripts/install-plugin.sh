#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "==> Building plugin bundle..."
python3 "${REPO_DIR}/scripts/build-plugin.py"

HERMES_HOME="${HOME}/.hermes"
SRC_PLUGIN="${HERMES_HOME}/plugins/office-3d"
LIVE_DESKTOP_PLUGIN="${HERMES_HOME}/desktop-plugins/office-3d"

echo "==> Syncing to ${SRC_PLUGIN}..."
mkdir -p "${SRC_PLUGIN}/desktop"
mkdir -p "${SRC_PLUGIN}/dashboard/dist"
mkdir -p "${LIVE_DESKTOP_PLUGIN}"

cp "${REPO_DIR}/desktop/plugin.js" "${SRC_PLUGIN}/desktop/plugin.js"
cp "${REPO_DIR}/dashboard/manifest.json" "${SRC_PLUGIN}/dashboard/manifest.json"
cp "${REPO_DIR}/dashboard/dist/index.js" "${SRC_PLUGIN}/dashboard/dist/index.js"

# Write both copies for immediate hot reload (as per hermes-desktop-plugins skill)
cp "${REPO_DIR}/desktop/plugin.js" "${LIVE_DESKTOP_PLUGIN}/plugin.js"

echo "==> Enabling office-3d in ~/.hermes/config.yaml..."
PYTHON_BIN="python3"
if [ -x "${HERMES_HOME}/hermes-agent/venv/bin/python" ]; then
    PYTHON_BIN="${HERMES_HOME}/hermes-agent/venv/bin/python"
fi

"${PYTHON_BIN}" -c "
import yaml
from pathlib import Path

cfg_path = Path.home() / '.hermes' / 'config.yaml'
if cfg_path.exists():
    data = yaml.safe_load(cfg_path.read_text(encoding='utf-8')) or {}
    plugins = data.get('plugins', {})
    enabled = plugins.get('enabled', [])
    if 'office-3d' not in enabled:
        enabled.append('office-3d')
        plugins['enabled'] = enabled
        data['plugins'] = plugins
        cfg_path.write_text(yaml.dump(data, sort_keys=False), encoding='utf-8')
        print('    [OK] office-3d added to plugins.enabled')
    else:
        print('    [OK] office-3d already present in plugins.enabled')
else:
    print('    [WARN] ~/.hermes/config.yaml not found')
"

echo "==> Plugin office-3d successfully installed and activated!"
