# Technical Architecture

## Current status
Engine-agnostic starter architecture. No engine or language has been selected yet.

## Suggested logical layers
- **Core:** application lifecycle, configuration, event bus, utilities
- **Scenes:** title, world, battle, menus, settings
- **Entities:** player, NPCs, enemies, interactables
- **Systems:** movement, combat, dialogue, quests, inventory, progression, save/load
- **Assets:** sprites, tilesets, audio, fonts, UI, effects

## Architecture principles
1. Keep gameplay rules separate from presentation.
2. Prefer small systems with explicit responsibilities.
3. Store tunable values in data/configuration rather than hard-coding them.
4. Keep save data versioned so it can be migrated.
5. Avoid engine-specific abstractions until the engine is selected.

## Proposed source layout
```text
src/
  core/
  entities/
  systems/
  scenes/
  data/
  ui/
tests/
```

## Next technical decision
Choose the engine, then replace this logical layout with its idiomatic project structure and add a minimal build/run guide.
