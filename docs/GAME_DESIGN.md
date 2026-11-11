# Game Design Document

## High concept
A 2D fantasy RPG built with crisp pixel art and a consistent 64×64 px character-sprite canvas. The player explores a connected world, meets NPCs, completes quests, gathers equipment, and fights enemies.

## Design pillars
1. **Exploration:** maps reward curiosity with secrets, landmarks, and optional encounters.
2. **Character progression:** experience, equipment, skills, and meaningful upgrades.
3. **Readable combat:** clear enemy telegraphs, understandable status effects, and responsive feedback.
4. **Cohesive pixel art:** consistent scale, palette, outline, lighting, and animation timing.

## Core gameplay loop
Explore area → discover NPCs, loot, and encounters → complete quests or battle → earn experience and items → upgrade character → unlock new areas.

## Initial systems
- Player movement and interaction
- World maps, collision, and transitions
- Dialogue and quest tracking
- Inventory and equipment
- Enemy AI and combat
- Save/load
- Audio, UI, and settings

## Combat direction
Start with a modular combat layer. Turn-based combat is a proposed baseline, not a locked decision; confirm the combat model before implementing detailed battle logic.

## Art requirements
- Character canvas: 64×64 px.
- Keep a consistent origin/pivot across animation frames.
- Initial animation set: idle, walk, attack, hurt, and defeat.
- Define tile size separately from character canvas size.
- Export source files and runtime-ready files in clearly named folders.

## Open decisions
- Game engine and target platforms
- Combat model and progression formula
- World setting, story, and playable character
- Tile grid dimensions and camera scale
- Multiplayer scope (if any)
