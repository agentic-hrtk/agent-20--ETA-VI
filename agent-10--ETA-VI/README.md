# ETA-VI

A single-player sci-fi RPG set aboard a remote deep-space research station that has gone dark. You play as a lone operative dispatched to find out why — and what you find will change everything.

---

## Overview

**ETA-VI** (Estimated Time of Arrival — Station Six) is a story-driven RPG combining atmospheric exploration, reactive combat, and branching narrative. The station is alive with environmental storytelling, hostile synthetic entities, and morally fractured survivors. Every choice shapes what remains of ETA-VI — and whether you make it off alive.

| | |
|---|---|
| **Engine** | Unity 6 (C#) |
| **Platform** | PC / macOS (Steam) |
| **Genre** | Sci-fi RPG |
| **Perspective** | Third-person, over-the-shoulder |
| **Mode** | Single-player |

---

## Features

- **Branching narrative** — Major decisions are permanent. Factions remember, survivors react, and the station's fate shifts with your choices.
- **Hybrid combat** — Seamlessly toggle between real-time action and tactical pause-and-command mode depending on your playstyle.
- **Deep character build** — Allocate points across six skill trees (Tactics, Engineering, Biotech, Psi, Diplomacy, Stealth) that unlock unique solutions to almost every obstacle.
- **Environmental storytelling** — The station's logs, debris fields, and corrupted AI terminals reconstruct what happened before you arrived.
- **Dynamic AI** — Enemy synthetics adapt to player behavior — they learn patrol patterns you've exploited and call for reinforcements under pressure.
- **Modular station layout** — Six distinct station sectors, each with its own atmosphere, faction presence, and escalating threat level.
- **Consequence system** — NPCs have survival states. If a survivor dies because of your negligence, their resources and quest lines are permanently lost.

---

## Lore

> *"Station ETA-VI. Designation: Deep Research Outpost, Class Omega. Last confirmed transmission: 47 days ago. Crew manifest: 312 personnel. Current response count: 0."*

Built at the edge of the Kerath Expanse, ETA-VI was humanity's furthest foothold — a classified facility running experiments the Earth Coalition would never sanction closer to home. When all contact ceased, the Coalition sent one asset to avoid drawing attention.

You are that asset.

The station is not empty.

---

## Sectors

| Sector | Description |
|--------|-------------|
| **Arrival Bay** | Docking and logistics — your entry point, heavily damaged |
| **Habitation Ring** | Crew quarters and common areas — survivors may be found here |
| **Research Core** | Labs and data vaults — the heart of the conspiracy |
| **Synthetic Works** | Manufacturing floor for station automata — now fully rogue |
| **Command Spine** | Operations, communications, and the station AI: VERAN |
| **The Deep** | Restricted sub-levels — classified experiments, locked behind the highest clearance |

---

## Getting Started

### Prerequisites

- Unity 6.0.0 or later
- .NET 8 SDK
- Git LFS (for binary assets)

### Setup

```bash
git clone https://github.com/your-org/ETA-VI.git
cd ETA-VI
git lfs pull
```

Open the project in Unity Hub by pointing it at the cloned directory. Use the **MainMenu** scene as the entry point (`Assets/Scenes/MainMenu.unity`).

### Build

1. Open **File → Build Settings**
2. Select target platform (Windows / macOS)
3. Click **Build** — output goes to `Builds/`

---

## Project Structure

```
ETA-VI/
├── Assets/
│   ├── Scripts/          # All C# game logic (see ARCHITECTURE.md)
│   ├── Scenes/           # Unity scene files per sector
│   ├── Prefabs/          # Reusable GameObjects
│   ├── Art/              # Models, textures, materials, VFX
│   ├── Audio/            # Music, SFX, ambient tracks
│   ├── Animations/       # Animator controllers and clips
│   ├── Data/             # ScriptableObjects (items, quests, dialogue)
│   └── Resources/        # Runtime-loaded assets
├── Packages/             # Unity package manifest
├── ProjectSettings/      # Unity project configuration
├── ARCHITECTURE.md       # System design and code structure
└── README.md
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch strategy, code style, and PR guidelines.

---

## License

TBD — proprietary until public release.
