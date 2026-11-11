# Art and Asset Guidelines

## Sprite standard
- Character canvas: **64×64 px**.
- Use nearest-neighbor scaling; avoid unintended blur.
- Keep feet baseline, pivot, and framing consistent across character animations.
- Make silhouettes recognizable at native resolution.

## Palette and lighting
- Use a limited, reusable palette per environment or character.
- Maintain consistent light direction.
- Reserve high-contrast colors for important gameplay information.

## Animation naming
Use descriptive names such as:
- `player_idle_down_00.png`
- `player_walk_down_00.png`
- `goblin_attack_left_02.png`

## Asset organization
Separate editable source files from exported runtime assets. Include a short README for any asset pack with dimensions, frame count, license, and attribution.

## Important distinction
64×64 px is the character canvas standard. Tiles, portraits, icons, effects, and UI may use other dimensions when documented.
