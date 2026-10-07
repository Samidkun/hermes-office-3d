# HANDOFF.md — Planning → Execution Contract

> Produced by `sop-planning` (P6), consumed by `sop-execution` (E0).
> Every section is filled, or marked `N/A — <reason>`. **"TBD" is forbidden.**
> An open question becomes a **Ruling** (decision + reason), never a gap.
> Frozen at handoff; changes are amendments recorded in §12.

---

## 1. Identity

| Field | Value |
|-------|-------|
| Project | Hermes Pixel Office (`hermes-pixel-office`) |
| Tier | T1 — Client / Deliverable |
| Ceremony level | M — Standard |
| Spec level | spec-anchored |
| Team size | Solo (Samid) |
| Stack | Hermes Desktop Plugin (ESM vanilla), HTML5 Canvas 2D Pixel Art Engine (12 FPS, Offscreen Blit, Y-sorted) |
| Constitution | `/mnt/data/01_Projects/Porto/hermes-office-3d/CONSTITUTION.md` |
| Handoff date | 2026-10-07 |
| Frozen by | Samid & Hermes Agent |

---

## 2. Goal & Scope

- **Goal (one sentence):** Membangun Hermes Desktop plugin yang menampilkan ruang kantor 2.5D Isometric Pixel Art interaktif secara real-time untuk memantau parent orchestrator dan dynamic subagents dengan konsumsi resource ultra-ringan (0% GPU, <3% CPU, 12 FPS, zero port).
- **In scope:**
  - Registrasi plugin Hermes Desktop (`desktop/plugin.js`) ke area workspace dan panes/titlebar.
  - Runtime 2.5D Canvas Isometric di dalam sandboxed iframe (`office_scene.html`).
  - **Ultra-Lightweight Engine:**
    - Frame rate dikunci pada 12–15 FPS (menghemat 80% daya).
    - Offscreen Canvas Blitting (ruangan statis dirasterisasi sekali ke memory buffer, frame loop hanya copy-paste bitmap).
    - Auto-sleep via `document.hidden` (0% CPU/GPU saat tab diminimize atau tidak terlihat).
    - Pure Canvas 2D murni (tanpa WebGL, GPU load 0%, laptop tetap dingin).
  - Procedural Pixel Art Sprites: Meja Boss, Meja Cubicle, War Room Table, Server Blade Rack, Espresso Coffee Bar, Water Cooler, Sofa Lounge, Potted Plants, Whiteboard Kanban.
  - Karakter Pixel Art Retro (Habbo/Kairosoft Style): Walk cycle kaki & bobbing, hands typing di keyboard, coffee sipping, speech bubbles komik.
  - Autonomous Waypoint Navigation: Karakter berjalan fisik antar zona kantor (Workstations, War Room, Pantry, Server Bay).
  - Telemetry HUD / Inspector: Menampilkan role, model, current tool, runtime elapsed time, task goal, dan activity log saat agen diklik.
  - Drag pan & zoom navigation.
  - Gateway Event Adapter: Menangkap `ctx.onEvent('*')` dan mentransformasikannya ke visualizer.
- **Out of scope (explicit):**
  - Mengunduh aset 3D GLTF eksternal berat (memakai canvas 2D pixel art ringan).
  - WebGL / Three.js 3D rendering (dieliminasi demi performa baterai & suhu laptop).
  - Input teks / prompt injection dua arah dari dalam kanvas (v1 fokus pada observabilitas/telemetri).
  - Server HTTP / WebSocket eksternal (menggunakan `postMessage` lokal antar iframe).
- **Definition of done (tier-based):**
  - Plugin ter-load otomatis saat Hermes Desktop dibuka.
  - Membuka workspace tab menampilkan kantor 2.5D pixel art tajam, stabil 12 FPS, CPU < 3%, GPU 0%.
  - Saat ada subagent spawn di Hermes, karakter pixel baru otomatis jalan masuk ke mejanya.
  - Seluruh Acceptance Criteria (AC-1 s/d AC-10) terverifikasi lolos.

---

## 2b. Boundaries

- **Always:**
  - Berjalan mandiri tanpa require port HTTP baru di localhost.
  - Mengisolasi canvas di dalam `iframe` agar UI Hermes Desktop tahan crash.
  - Menggunakan rendering tajam `image-rendering: pixelated`.
  - Menghentikan render loop saat tab tidak terlihat (`document.hidden === true`).
- **Ask first:**
  - Penambahan dependensi biner/native node-gyp.
- **Never:**
  - Menggunakan WebGL loop tak terkontrol yang memicu spike GPU iGPU/dGPU.
  - Menggunakan styling warna neon AI generik ("vibecode purple").
  - Menghapus atau memodifikasi file plugin pengguna lain di `~/.hermes/plugins/`.

---

## 2c. Capability Map

| Module id | Responsibility | Depends on |
|---|---|---|
| `plugin-core` | Registrasi plugin ke `@hermes/plugin-sdk`, workspace tab, & message bridge | — |
| `event-mapper` | Menerjemahkan event Hermes Gateway (`subagent.*`, `delegate.*`, `tool.*`) ke envelope visualizer | `plugin-core` |
| `isometric-engine` | 2.5D Canvas engine, tile grid, camera pan & zoom, depth sorting (Y-sort), 12 FPS throttle, offscreen blit | — |
| `office-sprites` | Pixel art sprites (desks, conference table, servers, coffee bar, couch, plants) | `isometric-engine` |
| `character-agent` | Karakter pixel art dev (walk cycles, typing, coffee, speech bubbles, waypoints) | `isometric-engine`, `office-sprites` |
| `telemetry-hud` | Panel inspeksi real-time (model, status, tools, logs) & scenario triggers | `character-agent`, `event-mapper` |

Build order: `isometric-engine` + `office-sprites` → `character-agent` → `telemetry-hud` → `plugin-core` + `event-mapper`

---

## 3. Prompt-Roast Result

- **Six-axis score:** 12/12 (Clear, specific & performance-anchored)
- **Gaps named & answered:**
  - Visual pivot disetujui: **2.5D Isometric Pixel Art Retro** (Habbo / Kairosoft style).
  - Performance requirement: Mencegah spike GPU dengan membuang WebGL, throttling 12 FPS, offscreen blitting, dan auto-sleep.
  - Waypoint navigation: Karakter berjalan fisik antar zona kantor (Workstations, War Room, Pantry, Server Bay).
- **False premise check:** Valid.
- **Assumptions surfaced (Rulings):**
  - *Ruling 1:* Menggunakan HTML5 Canvas 2D beresolusi tajam (`image-rendering: pixelated`) dengan offscreen buffer rendering untuk beban CPU < 3%.
  - *Ruling 2:* Depth sorting (Y-sorting) per-frame memastikan karakter dan furnitur tidak pernah tembus/clipping.
  - *Ruling 3:* Frame rate dikunci pada 12 FPS (tidak perlu 60 FPS untuk visual ambient monitoring).
- **Clarify gate (P1.5):** Passed.

---

## 4. Design Contract (UI)

### 4a. `DESIGN.md` Spine
- **Subject / Audience / Job:** Developer observability tool bergaya retro pixel art kantor virtual untuk memantau orkestrator dan subagen AI.
- **Voice:** Nostalgic, Grounded, Expressive, Living Sim.
- **Token Spine:** Mengacu pada `/mnt/data/01_Projects/Porto/hermes-office-3d/DESIGN.md`.
- **Signature Bet:** Autonomous Waypoint Navigation + Comic Speech Bubbles + Depth-Sorted Pixel Art Sprites + 12 FPS Offscreen Blit Engine.
- **Knobs:** `DESIGN_VARIANCE = 5`, `VISUAL_DENSITY = 7`, `MOTION_INTENSITY = 4`.
- **Anti-Slop Test:** Passed (retro pixel art klasik dengan depth sorting, bukan 3D silinder generik).

### 4a-bis. Screen Inventory (P2.0)
| # | Screen id | Screen | Archetype | Primary job | Entry from | States | AC | Mockup | ACC |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `office-workspace` | Pixel Office Simulator | Workspace / Canvas | Observability real-time multi-agent | TitleBar / Pane | Focus Sprint, War Room, Coffee Break, Review, Incident | AC-1 - AC-10 | `preview/mockup/office-workspace.html` | APPROVED (2026-10-07) |

### 4a-ter. Mockup & Approval Gate (P2.1)
- **Renderer used:** HTML5 Canvas 2D Isometric Pixel Art
- **Approved screens:** `office-workspace` (approved 2026-10-07 by Samid)
- **Screens NOT yet approved:** none

---

## 5. Acceptance Criteria — EARS, Binary-Testable

| Id | Pattern | EARS statement | Verify |
|---|---|---|---|
| AC-1 | event | WHEN user membuka tab *Pixel Office*, THE plugin SHALL merender ruang kantor 2.5D isometrik lengkap dengan zona meja, war room, dan pantry dalam waktu < 400ms. | Canvas context 2D created, initial frame rendered without errors. |
| AC-2 | state | WHILE kursor di-drag di area canvas, THE camera SHALL melakukan panning halus dan roda mouse melakukan zoom in/out. | Mouse event menggeser offset panX/panY dan zoom canvas. |
| AC-3 | event | WHEN mode *War Room Standup* aktif, THE karakter-karakter agen SHALL berjalan kaki secara fisik ke meja rapat kaca dan duduk melingkar. | Agen mentransisikan koordinat gx/gy ke waypoint meeting room dengan animasi jalan. |
| AC-4 | state | WHILE agen berada di status `coding`, THE agen SHALL duduk di meja kerja, animasi tangan mengetik di keyboard, dan monitor berkedip scanlines. | Status coding mengaktifkan animasi typing dan screen glow. |
| AC-5 | state | WHEN agen berada di status `idle_coffee`, THE agen SHALL berjalan ke pantry/sofa dan menampilkan gestur memegang/menyeruput cangkir kopi. | Status idle_coffee memindahkan agen ke koordinat pantry dan menampilkan mug. |
| AC-6 | event | WHEN agen memproses task penting, THE agen SHALL menampilkan speech bubble komik di atas kepalanya berisi ringkasan aksi/pikirannya. | Speech bubble dirender pada koordinat di atas kepala agen. |
| AC-7 | event | WHEN user mengklik karakter agen mana pun, THE sistem SHALL membuka panel inspector yang menampilkan: ID, Model, State, Zone, Tool Call, dan Activity Log. | Hit detection memilih agen dan membuka HUD inspector. |
| AC-8 | ubiquitous | THE plugin SHALL berjalan secara mandiri tanpa memerlukan server HTTP terpisah di port lokal. | Plugin berfungsi native dari Hermes Desktop tanpa subprocess CLI tambahan. |
| AC-9 | state | WHILE visualizer aktif, THE engine SHALL mengunci render loop pada 12–15 FPS dan menggunakan offscreen canvas blitting untuk menjamin beban CPU < 3% dan GPU 0%. | Frame timer membatasi draw call maksimal 15 per detik. |
| AC-10 | event | WHEN tab/window disembunyikan (`document.hidden === true`), THE render loop SHALL dijeda (paused) sehingga konsumsi CPU/GPU menjadi 0%. | Page visibility listener membatalkan requestAnimationFrame saat hidden. |

---

## 5b. Drift Contract (spec-drift-gate)

- **Spec artifact path:** `/mnt/data/01_Projects/Porto/hermes-office-3d/HANDOFF.md`
- **Criteria live in:** §5 Acceptance Criteria.
- **Rule:** Perubahan fitur wajib memperbarui `HANDOFF.md` di commit yang sama.
- **Drift gate command:** `bash ~/.hermes/skills/software-development/web-app-sop/scripts/e0-validate.sh /mnt/data/01_Projects/Porto/hermes-office-3d/HANDOFF.md`

---

## 6. Feature Completeness

- **In scope:**
  - 2.5D Isometric Canvas 2D engine dengan Y-sort depth ordering.
  - Procedural pixel-art furniture sprites & characters.
  - Multi-zone office: Workstation, War Room, Pantry, Server Bay, Whiteboard.
  - Waypoint movement & walk cycles.
  - Live comic speech bubbles.
  - Inspector telemetry HUD.
  - 12 FPS throttle & Offscreen canvas blit.
  - Auto-sleep saat background tab.
- **Deliberate exclusions:**
  - 3D WebGL meshes / skeletal rig (dieliminasi demi performa baterai & suhu laptop).
  - Prompt dispatching interaktif dua arah (v1 murni observabilitas).

---

## 7. Interfaces & File Paths

### Files to Create:
1. `/mnt/data/01_Projects/Porto/hermes-office-3d/desktop/plugin.js` — Plugin host Hermes Desktop (ESM uncompiled).
2. `/mnt/data/01_Projects/Porto/hermes-office-3d/desktop/office_scene.html` — Sandboxed 2.5D Pixel Art Canvas.
3. `/mnt/data/01_Projects/Porto/hermes-office-3d/scripts/install-plugin.sh` — Script symlink/sync ke `~/.hermes/plugins/office-3d`.
4. `/mnt/data/01_Projects/Porto/hermes-office-3d/README.md` — Dokumentasi portofolio & cara pakai.

---

## 7b. Interface Contracts

- **Layers & responsibilities:**
  - `plugin.js` (Host Layer): Meregistrasikan pane / workspace tab di Hermes Desktop, menyadap `ctx.onEvent('*')` dari gateway, dan meneruskannya ke iframe via `window.postMessage`.
  - `office_scene.html` (Canvas Layer): Menerima pesan telemetry, mengupdate state koordinat/waypoint agent, merender canvas 2D 12 FPS, dan memancarkan event klik agen balik ke host.
- **Boundary contract (postMessage payload):**
  ```typescript
  interface TelemetryMessage {
    type: 'HERMES_EVENT' | 'AGENT_CLICK' | 'SET_SCENARIO';
    payload: {
      agentId: string;
      role: 'orchestrator' | 'worker';
      name?: string;
      model?: string;
      state: 'coding' | 'thinking' | 'meeting' | 'idle_coffee' | 'done' | 'error';
      task?: string;
      tool?: string;
      speech?: string;
      logs?: Array<{ time: string; text: string }>;
    };
  }
  ```
- **Error envelope:** Pesan error ditampilkan pada banner status canvas jika format payload invalid.
- **Auth:** N/A (Iframe lokal sandboxed tanpa komunikasi jaringan eksternal).
- **Enforcement:** TypeScript interface definition & postMessage event type assertions.

---

## 8. Constraints

- **Runtime Constraints:** Hermes Desktop Plugin runtime allowlist: `@hermes/plugin-sdk`, `react`, `react/jsx-runtime`.
- **No plugin.yaml:** Folder plugin dilarang menyertakan `plugin.yaml` agar tidak dideteksi sebagai agent plugin yang membutuhkan `__init__.py`.
- **Canvas Rendering:** Murni Canvas 2D dengan `image-rendering: pixelated` dan zoom ratio 2:1.
- **Performance Budget:** Frame rate dibatasi 12–15 FPS, CPU usage < 3%, GPU usage 0%.

---

## 9. Plan Artifact

- **Plan required:** Yes
- **Path to plan:** Terangkum dalam task berikut:
  - **Task 1: Core 2.5D Engine & Offscreen Blit Architecture**
    - Implementasi Canvas 2D engine dengan 12 FPS throttler (`requestAnimationFrame` + delta timing).
    - Implementasi `OffscreenCanvas` rasterizer untuk lantai dan furnitur statis.
    - Pasang `document.visibilitychange` listener untuk auto-sleep (0% usage).
  - **Task 2: Character Sprite System & Waypoint Pathing**
    - Buat generator karakter pixel dev (kepala, badan, lanyard/tie, walk cycle bobbing).
    - Buat state machine: `coding` (ngetik), `meeting` (gesture tangan), `idle_coffee` (mug), `done` (hands up), `error` (x eyes).
    - Implementasi interpolasi waypoint koordinat antar zona.
  - **Task 3: Speech Bubbles & Telemetry HUD**
    - Dynamic comic speech bubbles di atas kepala karakter.
    - Raycast/hit detection klik karakter untuk membuka HUD Inspector.
  - **Task 4: Hermes Desktop Plugin Integration**
    - Bikin `desktop/plugin.js` yang mengekspos tombol ke Header/Activity bar.
    - Hubungkan `host.openWorkspace()` dengan sandboxed iframe `office_scene.html`.
    - Terjemahkan event gateway (`ctx.onEvent`) ke `postMessage` protocol.
  - **Task 5: Packaging & Installation Script**
    - Bikin `scripts/install-plugin.sh` untuk symlink ke `~/.hermes/plugins/office-3d`.
    - Tulis `README.md` dokumentasi portofolio lengkap dengan arsitektur & screenshot.

---

## 10. Factory Bootstrap

- **Status:** Deferred (Plugin murni file statis ESM + HTML/JS tanpa build step bundler).

---

## 11. Accepted Risks

| Risk | Why accepted | Owner |
|---|---|---|
| Framerate 12 FPS tampak retro | Sesuai desain estetik retro 16-bit dan menjaga laptop tetap dingin saat ditinggal AFK | Samid |

---

## 12. Amendments (Changelog)

| Date | Change | Reason | Re-approved by |
|---|---|---|---|
| 2026-10-07 | Pivot dari Three.js 3D ke 2.5D Isometric Pixel Art | Menghilangkan clipping janky 3D dan menjaga GPU 0% / laptop dingin | Samid |

---

## 13. P7 Readiness Gate Checklist

- [x] Tier + team + ceremony level written (§1)
- [x] Spec level declared (§1)
- [x] Constitution present (§1)
- [x] Boundaries recorded (§2b)
- [x] Capability map approved (§2c)
- [x] Prompt-roast scored; gaps answered (§3)
- [x] False premise checked against repo (§3)
- [x] Assumptions surfaced; expensive ones are Rulings (§3)
- [x] Clarify gate passed (§3)
- [x] Brainstorm approval obtained, in writing (§2/P1)
- [x] Design contract present if UI exists; every state named (§4)
- [x] Acceptance criteria EARS-shaped, each with id + Verify (§5)
- [x] Drift contract recorded (§5b)
- [x] Feature Completeness walked; exclusions stated (§6)
- [x] Interfaces exact; no "similar to" (§7)
- [x] File paths listed (§7)
- [x] Constraints copied verbatim (§8)
- [x] No TBD/TODO anywhere — open questions are Rulings
- [x] Mockup visual verified & inspected in desktop preview pane

**Frozen:** [X]  ·  **Handoff path:** `/mnt/data/01_Projects/Porto/hermes-office-3d/HANDOFF.md`  ·  **Seen by human:** [X]
