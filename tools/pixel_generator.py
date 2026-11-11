#!/usr/bin/env python3
"""Procedural pixel-art generator for Pixel RPG 64x64.

Requires Pillow:
    python -m pip install -r tools/requirements.txt

Examples:
    python tools/pixel_generator.py sprite --output assets/characters/hero.png
    python tools/pixel_generator.py tileset --tile-size 16 --palette forest --output assets/tilesets/forest.png
    python tools/pixel_generator.py all --output-dir generated --seed 42
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw

PALETTES = {
    "forest": {
        "outline": "#263238", "skin": "#e9b98b", "hair": "#55352f",
        "cloth": "#4f9b68", "accent": "#e9c46a",
        "grass": ["#39734b", "#4f9657", "#70ad5b", "#2d5d42"],
        "dirt": ["#815b3c", "#a4774d", "#bd9360"],
        "water": ["#285f83", "#347fa1", "#55a6b8"],
        "sand": ["#c7aa68", "#dfc782", "#ead99b"],
        "stone": ["#59636b", "#77828a", "#9aa3a4"],
        "path": ["#9b744c", "#b58b5d", "#c69b68"],
    },
    "dungeon": {
        "outline": "#20212b", "skin": "#c99b83", "hair": "#34313e",
        "cloth": "#665a83", "accent": "#c28bdb",
        "grass": ["#3d5549", "#506d58", "#6d8060", "#2d403b"],
        "dirt": ["#51433f", "#6b5550", "#80685c"],
        "water": ["#263d59", "#345878", "#527a91"],
        "sand": ["#877b69", "#a39780", "#b8ad91"],
        "stone": ["#454653", "#626474", "#858696"],
        "path": ["#5a5051", "#756666", "#928080"],
    },
    "desert": {
        "outline": "#49352d", "skin": "#edbd91", "hair": "#67402e",
        "cloth": "#c16e43", "accent": "#e9d17b",
        "grass": ["#7d8a43", "#a0a34c", "#b8ad59", "#596d3d"],
        "dirt": ["#a66b43", "#bd8650", "#d1a365"],
        "water": ["#397b91", "#4e9eaa", "#78bec0"],
        "sand": ["#c49a55", "#dfbd75", "#f0d99a"],
        "stone": ["#827568", "#a3957d", "#c0b18d"],
        "path": ["#b17c49", "#c9955b", "#dbad70"],
    },
}

TERRAIN_NAMES = ["grass", "dirt", "water", "sand", "stone", "path"]


def rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def speckle(draw: ImageDraw.ImageDraw, rng: random.Random, size: int,
            colors: list[str], count: int, min_block: int = 1,
            max_block: int = 2) -> None:
    for _ in range(count):
        x, y = rng.randrange(size), rng.randrange(size)
        w = rng.randint(min_block, max_block)
        h = rng.randint(min_block, max_block)
        draw.rectangle((x, y, min(size - 1, x + w - 1), min(size - 1, y + h - 1)),
                       fill=rng.choice(colors))


def make_tile(kind: str, size: int, palette: dict, rng: random.Random) -> Image.Image:
    image = Image.new("RGBA", (size, size), rgb(palette[kind][0]) + (255,))
    draw = ImageDraw.Draw(image)
    colors = palette[kind]
    if kind == "grass":
        speckle(draw, rng, size, colors[1:], max(10, size * 2))
        # Small tufts
        for _ in range(max(2, size // 8)):
            x, y = rng.randrange(1, size - 1), rng.randrange(2, size - 1)
            draw.point((x, y), fill=colors[2])
            if y > 0:
                draw.point((x, y - 1), fill=colors[1])
    elif kind == "dirt":
        speckle(draw, rng, size, colors[1:], max(12, size * 2))
        for _ in range(max(2, size // 8)):
            x, y = rng.randrange(size), rng.randrange(size)
            draw.line((x, y, min(size - 1, x + 2), y), fill=colors[0], width=1)
    elif kind == "water":
        speckle(draw, rng, size, colors[1:], max(5, size))
        for y in range(3, size, max(5, size // 3)):
            x = rng.randrange(max(1, size // 3))
            draw.line((x, y, min(size - 1, x + size // 3), y), fill=colors[2], width=1)
    elif kind == "sand":
        speckle(draw, rng, size, colors[1:], max(8, size))
        for _ in range(max(2, size // 10)):
            x, y = rng.randrange(size), rng.randrange(size)
            draw.point((x, y), fill=colors[0])
    elif kind == "stone":
        # Simple irregular block pattern
        mid = size // 2
        draw.line((0, mid, size - 1, mid), fill=colors[0], width=1)
        draw.line((mid, 0, mid, mid), fill=colors[0], width=1)
        draw.line((size // 3, mid, size // 3, size - 1), fill=colors[0], width=1)
        speckle(draw, rng, size, colors[1:], max(5, size // 2))
        draw.line((1, 1, mid - 1, 1), fill=colors[2], width=1)
    elif kind == "path":
        speckle(draw, rng, size, colors[1:], max(10, size))
        for _ in range(max(2, size // 8)):
            x, y = rng.randrange(size), rng.randrange(size)
            draw.rectangle((x, y, min(size - 1, x + 1), min(size - 1, y + 1)),
                           fill=colors[0])
    return image


def make_tileset(tile_size: int, palette_name: str, seed: int,
                 columns: int = 4) -> tuple[Image.Image, list[dict]]:
    palette = PALETTES[palette_name]
    rows = (len(TERRAIN_NAMES) + columns - 1) // columns
    sheet = Image.new("RGBA", (columns * tile_size, rows * tile_size), (0, 0, 0, 0))
    metadata = []
    for index, kind in enumerate(TERRAIN_NAMES):
        rng = random.Random(seed + index * 997)
        tile = make_tile(kind, tile_size, palette, rng)
        x, y = (index % columns) * tile_size, (index // columns) * tile_size
        sheet.alpha_composite(tile, (x, y))
        metadata.append({
            "name": kind, "index": index, "x": x, "y": y,
            "width": tile_size, "height": tile_size,
        })
    return sheet, metadata


def make_character(seed: int, palette_name: str = "forest") -> Image.Image:
    """Create a simple transparent 64x64 top-down RPG hero placeholder."""
    rng = random.Random(seed)
    p = PALETTES[palette_name]
    image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)
    outline, skin, hair, cloth, accent = [rgb(p[k]) for k in
                                          ("outline", "skin", "hair", "cloth", "accent")]

    # Shadow
    d.ellipse((18, 51, 45, 58), fill=(20, 24, 28, 90))
    # Boots and legs
    d.rectangle((21, 43, 28, 53), fill=outline)
    d.rectangle((35, 43, 42, 53), fill=outline)
    d.rectangle((22, 45, 27, 51), fill=hair)
    d.rectangle((36, 45, 41, 51), fill=hair)
    # Body silhouette and tunic
    d.rectangle((17, 24, 46, 46), fill=outline)
    d.rectangle((19, 25, 44, 43), fill=cloth)
    d.rectangle((27, 27, 36, 43), fill=accent)
    # Arms
    d.rectangle((13, 28, 19, 40), fill=outline)
    d.rectangle((44, 28, 50, 40), fill=outline)
    d.rectangle((14, 29, 18, 38), fill=skin)
    d.rectangle((45, 29, 49, 38), fill=skin)
    # Head and hair
    d.rectangle((19, 7, 44, 29), fill=outline)
    d.rectangle((21, 9, 42, 27), fill=skin)
    d.rectangle((20, 7, 43, 15), fill=hair)
    d.rectangle((18, 12, 23, 22), fill=hair)
    d.rectangle((40, 12, 45, 22), fill=hair)
    # Eyes
    d.rectangle((25, 18, 28, 20), fill=outline)
    d.rectangle((35, 18, 38, 20), fill=outline)
    # Small hair highlight and belt buckle
    d.rectangle((26, 9, 31, 10), fill=accent)
    d.rectangle((29, 34, 34, 38), fill=accent)
    # Tiny seed-driven accessory pixels
    for _ in range(5):
        x, y = rng.choice([15, 16, 47, 48]), rng.randint(25, 42)
        d.point((x, y), fill=accent)
    return image


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate procedural pixel-art assets.")
    sub = parser.add_subparsers(dest="command", required=True)

    sprite = sub.add_parser("sprite", help="Generate a transparent 64x64 hero sprite.")
    sprite.add_argument("--output", default="generated/hero_64x64.png")
    sprite.add_argument("--palette", choices=PALETTES, default="forest")
    sprite.add_argument("--seed", type=int, default=42)

    tiles = sub.add_parser("tileset", help="Generate a terrain tileset sprite sheet.")
    tiles.add_argument("--output", default="generated/terrain_tileset.png")
    tiles.add_argument("--tile-size", type=int, choices=(16, 32), default=16)
    tiles.add_argument("--columns", type=int, default=4)
    tiles.add_argument("--palette", choices=PALETTES, default="forest")
    tiles.add_argument("--seed", type=int, default=42)

    all_assets = sub.add_parser("all", help="Generate a hero and terrain tileset.")
    all_assets.add_argument("--output-dir", default="generated")
    all_assets.add_argument("--tile-size", type=int, choices=(16, 32), default=16)
    all_assets.add_argument("--palette", choices=PALETTES, default="forest")
    all_assets.add_argument("--seed", type=int, default=42)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "sprite":
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        make_character(args.seed, args.palette).save(output)
        save_json(output.with_suffix(".json"), {
            "type": "character", "canvas": [64, 64],
            "palette": args.palette, "seed": args.seed,
            "note": "Procedural placeholder; replace or edit for final game art."
        })
        print(f"Generated sprite: {output}")
    elif args.command == "tileset":
        if args.columns < 1:
            raise SystemExit("--columns must be at least 1")
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        sheet, tiles = make_tileset(args.tile_size, args.palette, args.seed, args.columns)
        sheet.save(output)
        save_json(output.with_suffix(".json"), {
            "type": "terrain_tileset", "tile_size": args.tile_size,
            "sheet_size": list(sheet.size), "columns": args.columns,
            "palette": args.palette, "seed": args.seed, "tiles": tiles
        })
        print(f"Generated tileset: {output}")
    elif args.command == "all":
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        make_character(args.seed, args.palette).save(out / "hero_64x64.png")
        sheet, tiles = make_tileset(args.tile_size, args.palette, args.seed)
        sheet.save(out / "terrain_tileset.png")
        save_json(out / "terrain_tileset.json", {
            "type": "terrain_tileset", "tile_size": args.tile_size,
            "sheet_size": list(sheet.size), "columns": 4,
            "palette": args.palette, "seed": args.seed, "tiles": tiles
        })
        save_json(out / "hero_64x64.json", {
            "type": "character", "canvas": [64, 64],
            "palette": args.palette, "seed": args.seed
        })
        print(f"Generated starter assets in: {out.resolve()}")


if __name__ == "__main__":
    main()
