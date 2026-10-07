# Constitution: Hermes Agent Office (2.5D Pixel Art Edition)

## Immutable Principles

1. **Zero Extra Process & Zero Port Overhead:**
   Berjalan 100% native di dalam ekosistem Hermes Desktop via Plugin System. Tidak memerlukan server terpisah (`npm run dev`, `python server.py`, Next.js server, dsb). Langsung render begitu workspace dibuka.

2. **Ultra-Lightweight Performance (Cold Laptop Guarantee):**
   - **Throttled Frame Rate:** Dikunci pada 12–15 FPS (sesuai standar animasi game retro 16-bit). Memotong konsumsi CPU/GPU hingga 80%.
   - **Offscreen Canvas Blitting:** Elemen statis (lantai, dinding, meja, server, pantry) dirasterisasi SATU KALI ke buffer memori (`OffscreenCanvas`). Render loop hanya me-blit bitmap dan menggambar karakter yang bergerak.
   - **Auto-Sleep:** Menggunakan `Page Visibility API` (`document.hidden`). Saat tab tidak aktif atau diminimize, loop animasi berhenti total (0% CPU / 0% GPU).
   - **Pure Canvas 2D:** Bebas dari WebGL pipeline, shader compilation, dan VRAM overhead. GPU tetap di 0% dan suhu laptop tetap dingin.

3. **Pixel-Perfect Clarity (Zero 3D Clipping / Janky Math Meshes):**
   Menggunakan arsitektur 2.5D Isometric Pixel Art dengan depth-sorting (Y-sort `gx + gy`) per-frame. Menghilangkan bug clipping, pergeseran tulang, kaki melayang, dan kamera gepeng.

4. **Grounded Telemetry (No Fictional State):**
   Aktivitas karakter (Focus Coding, Walking, Standup Meeting, Coffee Break, Incident) memetakan state asli dari Hermes Gateway (`delegate.*`, `tool.*`, `ctx.onEvent`).

5. **Living Office Simulation:**
   Karakter memiliki AI waypoint navigation antar zona kantor (Workstations, War Room, Pantry Bar, Server Bay, Whiteboard) dengan dialog speech bubble real-time.
