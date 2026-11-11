# Pixel Generator (Python)

A small procedural pixel-art tool for generating starter character sprites and terrain tilesets for the Godot project.

## Requirements

- Python 3.10+
- Pillow

Install dependencies from the repository root:

```bash
python -m pip install -r tools/requirements.txt
```

## Commands

Generate a transparent 64×64 character sprite:

```bash
python tools/pixel_generator.py sprite --output assets/characters/hero.png --palette forest --seed 42
```

Generate a 16×16 terrain tileset (PNG sprite sheet):

```bash
python tools/pixel_generator.py tileset --tile-size 16 --palette forest --output assets/tilesets/forest.png --seed 42
```

Generate a 32×32 tileset with a dungeon palette:

```bash
python tools/pixel_generator.py tileset --tile-size 32 --palette dungeon --output assets/tilesets/dungeon.png
```

Generate the starter character and tileset together:

```bash
python tools/pixel_generator.py all --output-dir generated --tile-size 16 --palette forest --seed 42
```

## Included palettes

- `forest`
- `dungeon`
- `desert`

## Tiles included

The terrain sheet contains grass, dirt, water, sand, stone, and path. A matching JSON file records tile names, dimensions, and sprite-sheet coordinates. The JSON is intended as a reference for configuring Godot TileSet/TileMapLayer resources; it is not an imported Godot TileSet resource.

## Notes

- The character is a procedural placeholder, not finished production art.
- Reusing the same seed and options reproduces the same output.
- Generated PNGs use nearest-neighbor-friendly pixel dimensions and RGBA transparency where appropriate.
- You can edit the palettes and drawing functions in `tools/pixel_generator.py` to add new themes and asset types.
