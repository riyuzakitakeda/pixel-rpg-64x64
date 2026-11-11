# Technical Architecture

## Engine
- **Engine:** Godot 4.x
- **Language:** GDScript
- **Renderer:** Compatibility (OpenGL), selected for broad desktop/mobile support
- **Project entry:** `res://scenes/main.tscn`
- **Logical viewport:** 640×360, scaled to the window
- **Pixel-art filtering:** nearest-neighbor; 2D transforms and vertices snap to pixels

## Current project foundation
- `project.godot`: engine configuration, main scene, display and input settings
- `scenes/main.tscn`: initial entry scene and temporary control HUD
- `scenes/player.tscn`: reusable CharacterBody2D player scene
- `scripts/player/player.gd`: top-down movement prototype and placeholder drawing
- `scripts/core/game_manager.gd`: starting point for global game state

## Suggested logical layers
- **Core:** application lifecycle, configuration, event bus, utilities
- **Scenes:** title, world, battle, menus, settings
- **Entities:** player, NPCs, enemies, interactables
- **Systems:** movement, combat, dialogue, quests, inventory, progression, save/load
- **Assets:** sprites, tilesets, audio, fonts, UI, effects

## Godot conventions
1. Use scenes for reusable game objects and UI components.
2. Keep scripts small and focused; use composition before deep inheritance.
3. Use signals for communication between loosely coupled nodes.
4. Use Resources or data files for tunable content such as items, enemies, and skills.
5. Add global scripts through Project Settings → Autoload only when truly global.
6. Keep save data versioned so it can be migrated between game versions.

## Sprite and camera rules
- Character art canvas: 64×64 px.
- Tile dimensions are configured independently from the character canvas.
- Keep character pivots and feet baselines consistent across animation frames.
- Use nearest-neighbor filtering and integer scaling where possible to preserve crisp pixels.

## Next technical steps
- Replace the player placeholder with an animated 64×64 sprite.
- Add a TileMapLayer-based test map and collision.
- Implement interaction prompts and NPC dialogue.
- Add a scene transition flow and save/load prototype.
- Select and document the final target platforms and aspect-ratio behavior.
