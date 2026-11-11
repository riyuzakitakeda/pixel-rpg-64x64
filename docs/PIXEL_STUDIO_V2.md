# Pixel Studio v2

Pixel Studio v2 expands the original procedural generator with character customization, directional animation sheets, and 4-neighbor terrain autotiles.

## Install

```bash
python -m pip install -r tools/requirements.txt
```

## 1. Custom character

```bash
python tools/pixel_studio.py character --output assets/characters/hero.png --hair blonde --hair-style spiky --outfit armor --outfit-color blue --skin tan
```

Options:
- Hair: brown, black, blonde, red, blue, white
- Hair style: short, long, spiky
- Outfit: tunic, robe, armor
- Outfit color: green, blue, red, purple, black, white, gold
- Skin: light, tan, dark, pale
- Palette: forest, dungeon, desert

## 2. Four-direction animation sheet

```bash
python tools/pixel_studio.py animation --output assets/characters/hero_walk.png --frames 4
```

The output is a horizontal sequence per direction, arranged in four rows: down, left, right, up. Each frame is 64×64 px. A JSON sidecar contains frame coordinates.

This is a procedural motion placeholder. Review and hand-polish the frames before using them as final character animation.

## 3. Terrain autotiles

```bash
python tools/pixel_studio.py autotile --tile-size 16 --palette forest --output assets/tilesets/grass_autotile.png
```

Creates 16 variants using four-neighbor masks:
- North = bit 1
- East = bit 2
- South = bit 4
- West = bit 8

The atlas is 4×4 tiles, with JSON metadata for each mask and source rectangle. This is a basic four-neighbor prototype, not a full  blob/47-tile or Godot TileSet resource.

## Output

Each PNG is accompanied by a JSON sidecar describing its dimensions, settings, or atlas coordinates. Keep generated outputs in `assets/` only after reviewing them; use a separate working folder for experiments.
