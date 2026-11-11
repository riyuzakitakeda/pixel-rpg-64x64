# Pixel RPG 64x64

A 2D fantasy RPG built with **Godot 4.x** and a consistent **64×64 px character-sprite canvas**.

## Engine and project status
- Engine: Godot 4.x (GDScript)
- Renderer: Compatibility (OpenGL)
- Initial logical viewport: 640×360
- Art direction: crisp pixel art with nearest-neighbor texture filtering
- Current milestone: runnable project foundation and player movement prototype

## Open the project
1. Install Godot 4.x.
2. Clone or download this repository.
3. In Godot Project Manager, choose **Import** and select `project.godot`.
4. Open the project and press **F6** to run the current scene or **F5** to run the project.

## Controls
- Move: WASD or arrow keys

## Repository structure
- `assets/characters` — player and NPC sprites
- `assets/enemies` — monsters and bosses
- `assets/items` — weapons, equipment, consumables
- `assets/tilesets` — terrain, interiors, dungeon tiles
- `assets/ui` — icons, panels, HUD
- `assets/effects` — combat and environmental effects
- `assets/audio` — music and sound effects
- `docs` — design, roadmap, art, and technical documentation
- `scenes` — Godot scenes
- `scripts` — GDScript organized by responsibility
- `tests` — automated tests and validation

## Pixel-art rules
64×64 px is the target character canvas, not a requirement that every tile, UI element, or background use the same dimensions. Keep pivots, scale, palette, outline treatment, and lighting consistent. Use nearest-neighbor filtering for pixel-art textures.

## Pixel Generator
A Python + Pillow procedural generator for 64×64 character placeholders and terrain tilesets. See [Pixel Generator Guide](docs/PIXEL_GENERATOR.md).

Quick start:

\`\`\`bash
python -m pip install -r tools/requirements.txt
python tools/pixel_generator.py all --output-dir generated --tile-size 16 --palette forest --seed 42
\`\`\`

## Documentation
- [Game Design](docs/GAME_DESIGN.md)
- [Development Roadmap](docs/ROADMAP.md)
- [Art Guidelines](docs/ART_GUIDELINES.md)
- [Godot Technical Architecture](docs/TECHNICAL_ARCHITECTURE.md)

## Current prototype
The starter scene includes a placeholder player with 2D movement and a camera. Replace the placeholder drawing with the finished 64×64 sprite when the character asset is ready.
