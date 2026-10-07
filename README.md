# 🏢 Hermes Pixel Office (`office-3d`)

> **Retro 2.5D Isometric AI Agent Office & Living Telemetry Simulator** for Hermes Desktop.  
> Memantau kerja Parent Orchestrator & Autonomous Subagents dalam format visual kantor virtual ala *Habbo Hotel* dan *Kairosoft Game Dev Story*.

---

## ✨ Fitur Utama

- 🎮 **2.5D Isometric Retro Engine:** Menggunakan proyeksi isometrik klasik 2:1 dengan depth-sorting (`gx + gy`) per-frame untuk menjamin **nol 3D clipping** dan tampilan pixel art yang tajam (`image-rendering: pixelated`).
- ⚡ **Ultra-Lightweight & Hemat Baterai:**
  - **12 FPS Throttle:** Frame rate dikunci pada 12 FPS, memangkas beban CPU/GPU hingga 80%.
  - **Offscreen Canvas Blitting:** Seluruh ubin lantai dan furnitur statis dirasterisasi sekali ke memory buffer (`OffscreenCanvas`), render loop hanya me-blit bitmap dan menggambar karakter.
  - **Auto-Sleep:** Menggunakan `Page Visibility API` (`document.hidden`). Render loop otomatis dijeda saat tab diminimize atau berada di background (0% CPU / 0% GPU).
  - **Zero WebGL Overhead:** Pure Canvas 2D murni, bebas dari shader compilation dan VRAM memory leaks.
- 🚶 **Autonomous Waypoint Navigation:** Karakter dev berjalan fisik melintasi zona kantor sesuai state tugas:
  - **Focus Sprint:** Duduk di workstation masing-masing dan mengetik cepat di keyboard.
  - **War Room Standup:** Berdiri dan berjalan ke ruang rapat kaca pod untuk berdiskusi di meja bundar.
  - **Pantry Coffee Break:** Berjalan ke mesin espresso merah, dispenser galon air, atau sofa santai.
  - **Pair Review:** QA berjalan mendatangi meja SecOps untuk review diff pull request.
  - **Production Incident:** Lemari server bay berkedip panik, agen bersiaga mitigasi crash.
- 💬 **Live Comic Speech Bubbles:** Menampilkan pikiran, aksi, dan tool call nyata dari agen tepat di atas kepalanya.
- 🔍 **Interactive Telemetry HUD:** Klik karakter mana pun untuk melihat detail mendalam: Model LLM, Current Tool, Runtime Uptime, Task Goal, dan Activity Logs.
- 🔌 **Zero Extra Server (Native Plugin):** 100% berjalan mandiri di dalam Hermes Desktop App tanpa perlu menjalankan `npm run dev` atau backend HTTP terpisah.

---

## 🏛️ Arsitektur Sistem

```text
[ Hermes Agent Gateway ]
         │ (ctx.onEvent('*') - subagent.start, delegate.*, tool.started)
         ▼
[ Hermes Desktop Plugin Host (desktop/plugin.js) ]
         │ (host.openWorkspace('office-3d:view') + postMessage)
         ▼
[ Sandboxed Iframe Runtime (desktop/office_scene.html) ]
    ├── OffscreenCanvas (Lantai, Dinding, Meja - Di-blit 1x)
    ├── Y-Sorted Entity Pipeline (Karakter, Server LEDs, Uap Kopi)
    ├── 12 FPS Frame Delta Throttler
    └── Page Visibility Auto-Sleep Listener
```

---

## 🚀 Panduan Penggunaan (End-User Guide)

### 1. Instalasi ke Hermes Desktop
Cukup jalankan script installer sekali dari terminal:
```bash
./scripts/install-plugin.sh
```
Script akan otomatis:
1. Mem-bundle engine visualizer ke format Hermes Desktop ESM plugin.
2. Menyinkronkan file ke `~/.hermes/plugins/office-3d/` dan `~/.hermes/desktop-plugins/office-3d/`.
3. Mengaktifkan `office-3d` di konfigurasi `~/.hermes/config.yaml`.

### 2. Membuka Workspace di Hermes Desktop
1. Buka aplikasi **Hermes Desktop**.
2. Pada panel sidebar / activity bar, pilih pane **"office"**.
3. Klik tombol **"Buka Lebar ↗"** untuk membuka tampilan workspace kantor beresolusi penuh.
4. Anda dapat melakukan:
   - **Pan / Geser Ruangan:** Drag mouse kiri di area kanvas.
   - **Zoom In / Out:** Scroll roda mouse.
   - **Inspeksi Agen:** Klik karakter agen mana pun untuk memfokuskan kamera dan membuka telemetry drawer di sisi kanan.

---

## 🛠️ Developer Runbook & Verification

### Menjalankan Uji Verifikasi Otomatis (AC-1 s/d AC-10)
```bash
python3 tests/test_plugin.py
```
Output:
```text
=== Running Hermes Pixel Office Verification Suite ===
[PASS] Plugin file structure & skill invariants
[PASS] AC-9 (12 FPS throttle & offscreen blit) and AC-10 (Auto-sleep)
[PASS] AC-3, AC-4, AC-5, AC-6 (Zones, waypoints, speech bubbles, states)
[PASS] AC-7, AC-8 (Inspector HUD & Gateway postMessage bridge)
=== ALL CHECKS PASSED (10/10) ===
```

### Validasi Drift SOP Handoff
```bash
bash ~/.hermes/skills/software-development/web-app-sop/scripts/e0-validate.sh HANDOFF.md
```

---

## 📜 Lisensi
MIT License © 2026 Samid & Hermes Agent.
