# ETA-VI — Architecture

This document describes the technical architecture and system design for ETA-VI. It is the authoritative reference for how major game systems are structured, how they communicate, and where their code lives.

---

## Table of Contents

1. [High-Level Overview](#1-high-level-overview)
2. [Directory Structure](#2-directory-structure)
3. [Core Systems](#3-core-systems)
4. [Player Systems](#4-player-systems)
5. [Combat System](#5-combat-system)
6. [AI & Enemy System](#6-ai--enemy-system)
7. [Narrative Systems](#7-narrative-systems)
8. [Inventory & Items](#8-inventory--items)
9. [Audio System](#9-audio-system)
10. [UI System](#10-ui-system)
11. [Save System](#11-save-system)
12. [Data Layer (ScriptableObjects)](#12-data-layer-scriptableobjects)
13. [Scene & Loading Architecture](#13-scene--loading-architecture)
14. [Inter-System Communication](#14-inter-system-communication)

---

## 1. High-Level Overview

ETA-VI is a single-player, Unity 6 C# project. The architecture is organized around three principles:

- **Separation of data from logic** — Game content (items, quests, dialogue) lives in ScriptableObjects, not in MonoBehaviour code.
- **Event-driven decoupling** — Systems communicate via a central `EventBus` rather than direct references, keeping dependencies unidirectional.
- **Singleton managers with scoped lifetimes** — Persistent singletons (GameManager, AudioManager, SaveSystem) survive scene loads via `DontDestroyOnLoad`. All other managers are scene-scoped and bootstrapped by their scene.

```
┌──────────────────────────────────────────────────────┐
│                     Game Layer                       │
│  Player ─── CombatSystem ─── AIDirector              │
│     │              │              │                  │
│     └──────────────┴──────────────┘                  │
│                     │                                │
│              EventBus (global)                       │
│                     │                                │
│  QuestManager ─ DialogueSystem ─ InventoryManager    │
│                     │                                │
│           Persistent Singletons Layer                │
│  GameManager ─ SaveSystem ─ AudioManager ─ UIManager │
└──────────────────────────────────────────────────────┘
```

---

## 2. Directory Structure

```
Assets/Scripts/
├── Core/
│   ├── GameManager.cs          # Global game state (paused, loading, active scene)
│   ├── EventBus.cs             # Typed publish/subscribe event system
│   ├── SceneLoader.cs          # Async scene loading with loading screen
│   ├── TimeManager.cs          # Pause, slow-mo, and tactical time control
│   └── Bootstrap.cs            # First-run scene initialization order
│
├── Player/
│   ├── PlayerController.cs     # Movement, camera, input routing
│   ├── PlayerStats.cs          # HP, stamina, skill levels, derived attributes
│   ├── PlayerSkillTree.cs      # Skill unlock logic and point allocation
│   ├── PlayerInteractor.cs     # Raycast-based world interaction (items, NPCs, terminals)
│   └── PlayerProgression.cs    # XP, leveling, milestone rewards
│
├── Combat/
│   ├── CombatManager.cs        # Mode switching (real-time ↔ tactical pause)
│   ├── AttackResolver.cs       # Hit detection, damage calculation, status effects
│   ├── Weapon.cs               # Base weapon class (melee, ranged, energy)
│   ├── Ability.cs              # Active/passive abilities tied to skill trees
│   ├── StatusEffectSystem.cs   # Burn, hack, stun, bleed — timed effect stack
│   └── CombatHUD.cs            # In-combat UI overlay (AP, threat, cooldowns)
│
├── AI/
│   ├── AIDirector.cs           # Global difficulty governor — scales aggression/patrolling
│   ├── EnemyController.cs      # Per-enemy state machine driver
│   ├── States/
│   │   ├── PatrolState.cs
│   │   ├── AlertState.cs
│   │   ├── CombatState.cs
│   │   ├── SearchState.cs
│   │   └── FleeState.cs
│   ├── PerceptionSystem.cs     # Sight/sound cone detection with memory
│   ├── ThreatMemory.cs         # Per-enemy record of observed player behavior
│   └── NavAgentWrapper.cs      # Unity NavMesh abstraction with dynamic obstacle support
│
├── Narrative/
│   ├── DialogueSystem.cs       # Dialogue runner — parses DialogueData, drives UI
│   ├── DialogueNode.cs         # Branching node: speaker, lines, conditions, outcomes
│   ├── QuestManager.cs         # Active quest tracking, objective state, completion hooks
│   ├── QuestObjective.cs       # Single trackable goal with completion predicate
│   ├── ConsequenceSystem.cs    # Evaluates and records player decisions with downstream effects
│   ├── FactionManager.cs       # Per-faction standing; affects NPC behavior and shop access
│   └── JournalManager.cs       # In-game log: lore entries, NPC profiles, terminal records
│
├── Inventory/
│   ├── InventoryManager.cs     # Add/remove/query items; fires EventBus events on change
│   ├── ItemStack.cs            # Runtime item instance with quantity and condition
│   ├── EquipmentManager.cs     # Handles equipped slots and stat deltas
│   └── CraftingSystem.cs       # Recipe evaluation and item synthesis
│
├── Audio/
│   ├── AudioManager.cs         # Persistent singleton; handles music, SFX, ambient layers
│   ├── MusicDirector.cs        # Adaptive music — transitions tracks based on game state
│   ├── SFXPool.cs              # Object-pooled AudioSource management
│   └── AmbienceLayer.cs        # Sector-specific looping ambience mixer
│
├── UI/
│   ├── UIManager.cs            # Screen stack: push/pop UI panels
│   ├── HUD.cs                  # In-game heads-up display (health, stamina, minimap)
│   ├── InventoryUI.cs          # Inventory grid panel
│   ├── DialogueUI.cs           # Dialogue box and choice selection
│   ├── QuestTrackerUI.cs       # Active objectives overlay
│   ├── PauseMenuUI.cs          # Pause screen with save/load/settings
│   └── LoadingScreenUI.cs      # Transition screen during scene loads
│
└── Save/
    ├── SaveSystem.cs           # Serialization/deserialization to disk (JSON + binary)
    ├── SaveData.cs             # Root serializable snapshot of all game state
    ├── PlayerSaveData.cs       # Player stats, position, inventory
    ├── WorldSaveData.cs        # Scene object states, NPC states, door/lock states
    └── NarrativeSaveData.cs    # Quest states, faction standings, consequence flags
```

---

## 3. Core Systems

### GameManager
Singleton. Owns the global state machine:

```
BOOT → MAIN_MENU → LOADING → PLAYING → PAUSED → GAME_OVER
```

Exposes `GameManager.Instance.State` and fires `GameStateChanged` events on the EventBus whenever state transitions occur. All other singletons listen to this rather than calling each other.

### EventBus
Generic typed pub/sub. No MonoBehaviour required — any C# class can subscribe.

```csharp
EventBus.Subscribe<CombatStartedEvent>(OnCombatStarted);
EventBus.Publish(new CombatStartedEvent { Initiator = enemy });
EventBus.Unsubscribe<CombatStartedEvent>(OnCombatStarted);
```

Key event families: `Combat*`, `Quest*`, `Dialogue*`, `Inventory*`, `Player*`, `Scene*`.

### TimeManager
Wraps `Time.timeScale`. Three modes: `Normal (1.0)`, `TacticalPause (0.0)`, `SlowMotion (0.25)`. The combat system drives this; UI and audio are exempt via `Time.unscaledDeltaTime`.

---

## 4. Player Systems

### PlayerController
Uses Unity's new Input System. Separates input reading (`PlayerInputReader`) from movement application (`PlayerController`) to allow AI-driven cutscene control and testing without hardware input.

### PlayerStats
All attributes are computed properties derived from a base value + equipment deltas + status effect modifiers. Nothing is stored redundantly. Skills (Tactics, Engineering, Biotech, Psi, Diplomacy, Stealth) are integers 0–10 that gate ability unlocks and dialogue options.

### PlayerInteractor
Single-responsibility raycast component. On `E` press, it queries `IInteractable` on the hit collider. The interaction itself lives in the target, not here.

---

## 5. Combat System

### Mode Switching
`CombatManager` toggles between **Real-Time** and **Tactical Pause** via `TimeManager`. In tactical pause, the player spends Action Points (AP) to queue commands; resuming executes them in sequence.

### Damage Pipeline

```
WeaponFire / AbilityActivate
        │
   AttackResolver
        ├── Hit detection (Physics.Raycast / OverlapSphere)
        ├── Damage formula: base × skill_multiplier × armor_reduction
        ├── Critical check (Tactics skill gates crit chance)
        └── StatusEffectSystem.Apply(effect, target, duration)
```

### Weapons
`Weapon` is a ScriptableObject-backed MonoBehaviour. Subclasses: `MeleeWeapon`, `RangedWeapon`, `EnergyWeapon`. Each defines `FireMode`, `DamageProfile`, and `AbilitySlots`.

---

## 6. AI & Enemy System

### State Machine
Each enemy runs a stack-based FSM via `EnemyController`. States are plain C# classes implementing `IEnemyState`:

```csharp
interface IEnemyState {
    void Enter(EnemyController ctx);
    void Tick(EnemyController ctx);
    void Exit(EnemyController ctx);
}
```

### AIDirector
Global singleton. Adjusts aggression across all active enemies based on how the player is performing. Prevents snowballing: if the player is struggling, patrol spacing increases; if the player is dominating, synthetics begin coordinating.

### ThreatMemory
Per-enemy rolling record of the last N observed player actions (attacks, paths, timing). Used to break patrol routines the player has exploited more than twice.

### PerceptionSystem
Cone-based sight (configurable angle/range/occlusion) plus radial sound detection. Awareness builds on a 0–100 scale: `<25` passive, `25–75` alerted, `>75` full combat. Awareness decays when the stimulus is lost.

---

## 7. Narrative Systems

### DialogueSystem
Loads `DialogueData` ScriptableObjects. Each node holds lines, speaker reference, optional condition predicates (skill checks, faction standing), and outcome callbacks (flag sets, quest triggers). The runner is decoupled from UI — it emits events that `DialogueUI` consumes.

### QuestManager
Quests are `QuestData` ScriptableObjects with a list of `QuestObjective` definitions. At runtime, `QuestManager` instantiates live `QuestInstance` objects tracking state. Completion predicates are evaluated each frame against the world state.

### ConsequenceSystem
Maintains a dictionary of named flags. Major player decisions publish a `DecisionMadeEvent` with the flag key and value. Downstream systems (dialogue conditions, NPC availability, ending evaluator) query flags — never query each other directly.

### FactionManager
Six factions aboard ETA-VI. Standing is an integer −100 to +100. Crossing thresholds unlocks or locks NPC interactions, shop tiers, and ending branches.

---

## 8. Inventory & Items

- Items are `ItemData` ScriptableObjects (id, name, description, icon, weight, type, effects).
- `InventoryManager` holds a `List<ItemStack>` capped by weight limit.
- Equipment slots: Head, Torso, Arms, Legs, Primary, Secondary, Utility × 3.
- Crafting recipes are `RecipeData` ScriptableObjects evaluated by `CraftingSystem`.

---

## 9. Audio System

### MusicDirector
Maintains a list of `MusicLayer` tracks. On `GameStateChanged` or sector transition, it crossfades to the appropriate track group. Combat triggers an additive percussion layer without cutting the ambient track.

### SFXPool
Fixed-size AudioSource pool. SFX requests go through `AudioManager.PlaySFX(clip, position)` — never `AudioSource.PlayClipAtPoint` (which creates and destroys GameObjects).

---

## 10. UI System

`UIManager` maintains a panel stack. `PushPanel(panel)` activates a panel and disables input on the one below. `PopPanel()` restores it. This naturally handles nested menus (inventory → item detail → crafting) without manual enable/disable management.

All panels inherit `UIPanel` base class with `OnShow()` / `OnHide()` lifecycle hooks.

---

## 11. Save System

Save slots are JSON files at `Application.persistentDataPath/saves/slot_N.json`. Binary blob for world object states (more compact). Autosave triggers on: sector transition, quest completion, dialogue end.

`SaveData` is the root object serialized per slot:

```
SaveData
├── PlayerSaveData      (stats, position, inventory, skill points)
├── WorldSaveData       (per-scene: object states, NPC states, locks)
└── NarrativeSaveData   (quest states, faction standings, consequence flags)
```

Systems implement `ISaveable` with `GetSaveData()` / `LoadSaveData(data)`. `SaveSystem` collects from all registered `ISaveable` instances on save; distributes on load.

---

## 12. Data Layer (ScriptableObjects)

All game content is data-driven via ScriptableObjects under `Assets/Data/`:

```
Data/
├── Items/          # ItemData per item
├── Weapons/        # WeaponData per weapon
├── Quests/         # QuestData per quest
├── Dialogue/       # DialogueData per conversation tree
├── Enemies/        # EnemyData (stats, drops, behavior profile)
├── Factions/       # FactionData (name, default standing, modifiers)
├── Recipes/        # RecipeData for crafting
└── Abilities/      # AbilityData per skill-tree ability
```

No game content is hardcoded. This makes content iteration, localization, and modding straightforward.

---

## 13. Scene & Loading Architecture

Each station sector is a separate Unity scene. Persistent systems live in a `_Core` scene loaded additively at boot and never unloaded. Sector scenes are loaded/unloaded additively as the player moves between areas.

```
_Core (always loaded)
├── GameManager
├── AudioManager
├── SaveSystem
├── UIManager
└── EventBus

Sector_ArrivalBay (loaded on enter, unloaded on exit)
Sector_HabitationRing
Sector_ResearchCore
Sector_SyntheticWorks
Sector_CommandSpine
Sector_TheDeep
```

`SceneLoader` handles the async load/unload cycle with a loading screen and optional preload of the next sector.

---

## 14. Inter-System Communication

| Pattern | When to use |
|---|---|
| **EventBus** | Cross-system notifications where the publisher shouldn't know who's listening (e.g., `ItemPickedUp`, `EnemyDied`) |
| **Direct reference** | Tightly coupled subsystems within the same domain (e.g., `CombatManager` calling `AttackResolver`) |
| **ScriptableObject events** | Designer-facing triggers that need to be wired in the Inspector without code |
| **Interface query** | Interaction pattern — `IInteractable`, `IDamageable`, `ISaveable` — avoids hard type coupling |

**Rule:** Systems must never hold a runtime reference to a system in a different domain. Cross-domain communication always goes through the EventBus.
