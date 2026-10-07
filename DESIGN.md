# DESIGN.md: Hermes Agent Office (2.5D Isometric Pixel Art Edition)

## 1. Subject, Audience & Primary Job
- **Subject:** 2.5D Isometric Pixel Art Virtual Office & Multi-Agent Telemetry for Hermes Agent.
- **Audience:** Developers and technical users running complex orchestrator & subagent workflows.
- **Primary Job:** Memberikan observabilitas real-time atas aktivitas agent (coding, meeting, break, error) dalam format pixel-art kantor retro (ala Habbo / Kairosoft) yang bersih, zero-bug, dan hidup.

## 2. Voice & Tone
- **Nostalgic & Grounded:** Hangat, estetik 16-bit retro developer office, detail furnitur kayu dan karpet slate.
- **Expressive:** Karakter pixel art memiliki siluet jelas, animasi jalan yang luwes, gestur ngetik di keyboard, dan speech bubbles komik.
- **Informative:** Status agent dan nama tool langsung terbaca di atas kepala karakter dan di panel telemetry inspector.

## 3. Visual System & Tilemap Tokens

### Isometric Grid
- Isometric Tile Dimensions: `64px × 32px` diamond ratio (2:1 classic isometric projection).
- Render Canvas: HTML5 Canvas 2D dengan `image-rendering: pixelated` dan zoom 2x/3x crisp scaling.

### Color Palette (Warm Studio Loft)
- Floor Parquet: `#2E3440` (Slate Wood) & `#3B4252` (Nordic Ash)
- Area Rug / Carpet: `#434C5E` dengan outline `#4C566A`
- Boss Workstation: `#5E81AC` (Walnut Trim) + Dual Monitors
- Worker Cubicles: `#D08770` (Warm Beechwood)
- Wall Slat & Panels: `#2E3440` (Dark Timber)
- UI Background: `#0B0D13` (Deep Obsidian)

### Semantics & Status Emissives
- `STATE_CODING`: `#06B6D4` (Cyan Electric / Active Typing)
- `STATE_THINKING`: `#F59E0B` (Amber Glow / Brainstorming)
- `STATE_MEETING`: `#A855F7` (Purple / Collaborative Standup)
- `STATE_IDLE`: `#64748B` (Muted Slate / Coffee Break)
- `STATE_DONE`: `#10B981` (Emerald Mint / Task Completed)
- `STATE_ERROR`: `#F43F5E` (Rose Alert / Incident Blocker)

## 4. One Signature Bet
- **Living Waypoint Navigation & Live Speech Bubbles:**
  Karakter AI secara fisik berjalan melintasi ruangan kantor menuju zona fungsional (Workstations, War Room Meja Bundar, Espresso Coffee Bar, Server Bay, dan Whiteboard Kanban) disertai speech bubble dialog yang memperlihatkan pemikiran dan aksi nyata agen.

## 5. Anti-Slop Enforcement
- Dilarang 3D math geometry primitives yang patah-patah dan tembus meja.
- Dilarang tombol emoji tanpa konteks.
- Dilarang warna neon AI acak ("vibecode purple").
- Semua data inspeksi menggunakan data nyata developer Indonesia.
