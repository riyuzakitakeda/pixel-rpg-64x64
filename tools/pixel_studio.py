#!/usr/bin/env python3
"""Pixel Studio v2: customizable 64x64 characters, directional animations and autotiles."""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from PIL import Image, ImageDraw

PALETTES = {
    "forest": {"outline":"#263238","skin":"#e9b98b","hair":"#55352f","cloth":"#4f9b68","accent":"#e9c46a","ground":"#39734b","edge":"#2d5d42","detail":"#70ad5b"},
    "dungeon": {"outline":"#20212b","skin":"#c99b83","hair":"#34313e","cloth":"#665a83","accent":"#c28bdb","ground":"#454653","edge":"#30313d","detail":"#858696"},
    "desert": {"outline":"#49352d","skin":"#edbd91","hair":"#67402e","cloth":"#c16e43","accent":"#e9d17b","ground":"#c49a55","edge":"#a77d43","detail":"#f0d99a"},
}
HAIR_COLORS = {"brown":"#55352f","black":"#29252b","blonde":"#d6ae55","red":"#a84c36","blue":"#456c9b","white":"#d7d6d0"}
OUTFIT_COLORS = {"green":"#4f9b68","blue":"#477fae","red":"#ad514b","purple":"#7960a5","black":"#41434c","white":"#c9c8bb","gold":"#b68b3c"}
SKIN_COLORS = {"light":"#f0c7a0","tan":"#c98f68","dark":"#86583f","pale":"#e3c9bd"}


def rgba(hex_color: str, alpha: int = 255):
    h=hex_color.lstrip("#")
    return tuple(int(h[i:i+2],16) for i in (0,2,4))+(alpha,)


def character(palette_name="forest", hair_color=None, outfit_color=None,
              skin_color=None, hair_style="short", outfit="tunic",
              direction="down", frame=0, seed=42):
    p=PALETTES[palette_name]
    outline=rgba(p["outline"]); skin=rgba(skin_color or p["skin"])
    hair=rgba(hair_color or p["hair"]); cloth=rgba(outfit_color or p["cloth"])
    accent=rgba(p["accent"])
    im=Image.new("RGBA",(64,64),(0,0,0,0)); d=ImageDraw.Draw(im)
    bob=[0,0,-1,0][frame%4]
    leg_shift=[0,1,0,-1][frame%4]
    # Ground shadow
    d.ellipse((18,52,45,58),fill=(18,22,25,90))
    # Legs and boots
    d.rectangle((21,43+leg_shift,28,53+leg_shift),fill=outline)
    d.rectangle((35,43-leg_shift,42,53-leg_shift),fill=outline)
    d.rectangle((22,46+leg_shift,27,51+leg_shift),fill=hair)
    d.rectangle((36,46-leg_shift,41,51-leg_shift),fill=hair)
    # Outfit silhouette
    d.rectangle((17,24+bob,46,46+bob),fill=outline)
    d.rectangle((19,25+bob,44,43+bob),fill=cloth)
    if outfit=="robe":
        d.polygon([(19,34+bob),(44,34+bob),(47,46+bob),(16,46+bob)],fill=cloth)
        d.line((19,35+bob,44,35+bob),fill=accent,width=2)
    elif outfit=="armor":
        d.rectangle((20,26+bob,43,42+bob),fill=cloth)
        d.rectangle((24,27+bob,39,30+bob),fill=accent)
        d.rectangle((28,31+bob,35,42+bob),fill=rgba(p["outline"]))
        d.rectangle((30,33+bob,33,37+bob),fill=accent)
    else:
        d.rectangle((27,27+bob,36,43+bob),fill=accent)
    # Arms move slightly in walk cycle
    arm=frame%2
    d.rectangle((13,28+bob+arm,19,40+bob+arm),fill=outline)
    d.rectangle((44,28+bob-arm,50,40+bob-arm),fill=outline)
    d.rectangle((14,29+bob+arm,18,38+bob+arm),fill=skin)
    d.rectangle((45,29+bob-arm,49,38+bob-arm),fill=skin)
    # Head
    d.rectangle((19,7+bob,44,29+bob),fill=outline)
    d.rectangle((21,9+bob,42,27+bob),fill=skin)
    # Hair styles
    if hair_style=="long":
        d.rectangle((18,8+bob,45,25+bob),fill=hair)
        d.rectangle((18,16+bob,22,31+bob),fill=hair)
        d.rectangle((41,16+bob,45,31+bob),fill=hair)
        d.rectangle((21,8+bob,42,14+bob),fill=hair)
    elif hair_style=="spiky":
        d.rectangle((20,10+bob,43,16+bob),fill=hair)
        d.polygon([(20,13+bob),(18,5+bob),(25,10+bob),(29,3+bob),(33,10+bob),(39,4+bob),(43,13+bob)],fill=hair)
        d.rectangle((18,13+bob,23,22+bob),fill=hair)
    else:
        d.rectangle((20,7+bob,43,15+bob),fill=hair)
        d.rectangle((18,12+bob,23,22+bob),fill=hair)
        d.rectangle((40,12+bob,45,22+bob),fill=hair)
    # Face and direction
    if direction=="down":
        d.rectangle((25,18+bob,28,20+bob),fill=outline); d.rectangle((35,18+bob,38,20+bob),fill=outline)
    elif direction=="up":
        d.rectangle((20,8+bob,43,24+bob),fill=hair)
    elif direction=="left":
        d.rectangle((23,18+bob,25,20+bob),fill=outline)
        d.rectangle((18,14+bob,23,24+bob),fill=hair)
    elif direction=="right":
        d.rectangle((38,18+bob,40,20+bob),fill=outline)
        d.rectangle((40,14+bob,45,24+bob),fill=hair)
    d.rectangle((29,34+bob,34,38+bob),fill=accent)
    return im


def make_animation(args):
    directions=["down","left","right","up"]
    frames=[]
    for direction in directions:
        for frame in range(args.frames):
            frames.append(character(args.palette,HAIR_COLORS[args.hair],OUTFIT_COLORS[args.outfit_color],
                                    SKIN_COLORS[args.skin],args.hair_style,args.outfit,
                                    direction,frame,args.seed))
    sheet=Image.new("RGBA",(64*args.frames,64*len(directions)),(0,0,0,0))
    meta=[]
    for i,im in enumerate(frames):
        x=(i%args.frames)*64; y=(i//args.frames)*64
        sheet.alpha_composite(im,(x,y))
        meta.append({"direction":directions[i//args.frames],"frame":i%args.frames,
                     "x":x,"y":y,"width":64,"height":64})
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); sheet.save(out)
    out.with_suffix(".json").write_text(json.dumps({"type":"character_animation","canvas":[64,64],
        "frames_per_direction":args.frames,"directions":directions,"layout":"rows=directions, columns=frames",
        "frames":meta},indent=2),encoding="utf-8")
    print(f"Saved animation sheet: {out} ({sheet.width}x{sheet.height})")


def make_autotile(args):
    """Create 16 four-neighbor masks. Bit order: N=1, E=2, S=4, W=8."""
    p=PALETTES[args.palette]; size=args.tile_size; cols=4; rows=4
    sheet=Image.new("RGBA",(cols*size,rows*size),(0,0,0,0))
    meta=[]
    for mask in range(16):
        tile=Image.new("RGBA",(size,size),rgba(p["ground"]))
        d=ImageDraw.Draw(tile); edge=rgba(p["edge"]); detail=rgba(p["detail"])
        t=max(2,size//5)
        # An edge is drawn where the matching neighbor bit is absent.
        if not mask&1: d.rectangle((0,0,size-1,t-1),fill=edge)
        if not mask&2: d.rectangle((size-t,0,size-1,size-1),fill=edge)
        if not mask&4: d.rectangle((0,size-t,size-1,size-1),fill=edge)
        if not mask&8: d.rectangle((0,0,t-1,size-1),fill=edge)
        # Small deterministic detail pixels
        rng=random.Random(args.seed+mask*31)
        for _ in range(max(2,size//8)):
            x=rng.randrange(t,size-t if size-t>t else size)
            y=rng.randrange(t,size-t if size-t>t else size)
            d.point((x,y),fill=detail)
        x=(mask%cols)*size; y=(mask//cols)*size
        sheet.alpha_composite(tile,(x,y))
        meta.append({"mask":mask,"neighbors":{"north":bool(mask&1),"east":bool(mask&2),
                    "south":bool(mask&4),"west":bool(mask&8)},
                    "x":x,"y":y,"width":size,"height":size})
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); sheet.save(out)
    out.with_suffix(".json").write_text(json.dumps({"type":"four_neighbor_autotile",
        "tile_size":size,"sheet_size":list(sheet.size),"mask_bits":{"north":1,"east":2,"south":4,"west":8},
        "tiles":meta},indent=2),encoding="utf-8")
    print(f"Saved 16-mask autotile sheet: {out}")


def parser():
    p=argparse.ArgumentParser(description="Pixel Studio v2 — RPG character and terrain asset generator")
    sub=p.add_subparsers(dest="command",required=True)
    a=sub.add_parser("character",help="Generate one customizable 64x64 character")
    a.add_argument("--output",default="generated/character.png")
    a.add_argument("--palette",choices=PALETTES,default="forest")
    a.add_argument("--hair",choices=HAIR_COLORS,default="brown")
    a.add_argument("--outfit-color",choices=OUTFIT_COLORS,default="green")
    a.add_argument("--skin",choices=SKIN_COLORS,default="light")
    a.add_argument("--hair-style",choices=["short","long","spiky"],default="short")
    a.add_argument("--outfit",choices=["tunic","robe","armor"],default="tunic")
    a.add_argument("--direction",choices=["down","up","left","right"],default="down")
    a.add_argument("--seed",type=int,default=42)
    b=sub.add_parser("animation",help="Generate 4-direction character animation sheet")
    b.add_argument("--output",default="generated/hero_walk_sheet.png")
    b.add_argument("--palette",choices=PALETTES,default="forest")
    b.add_argument("--hair",choices=HAIR_COLORS,default="brown")
    b.add_argument("--outfit-color",choices=OUTFIT_COLORS,default="green")
    b.add_argument("--skin",choices=SKIN_COLORS,default="light")
    b.add_argument("--hair-style",choices=["short","long","spiky"],default="short")
    b.add_argument("--outfit",choices=["tunic","robe","armor"],default="tunic")
    b.add_argument("--frames",type=int,choices=[2,4,6,8],default=4)
    b.add_argument("--seed",type=int,default=42)
    c=sub.add_parser("autotile",help="Generate 16 four-neighbor terrain masks")
    c.add_argument("--output",default="generated/grass_autotile.png")
    c.add_argument("--tile-size",type=int,choices=[16,32],default=16)
    c.add_argument("--palette",choices=PALETTES,default="forest")
    c.add_argument("--seed",type=int,default=42)
    return p


def main():
    args=parser().parse_args()
    if args.command=="character":
        im=character(args.palette,HAIR_COLORS[args.hair],OUTFIT_COLORS[args.outfit_color],
                     SKIN_COLORS[args.skin],args.hair_style,args.outfit,args.direction,0,args.seed)
        out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); im.save(out)
        out.with_suffix(".json").write_text(json.dumps({"type":"character","canvas":[64,64],
            "palette":args.palette,"hair":args.hair,"hair_style":args.hair_style,
            "outfit":args.outfit,"outfit_color":args.outfit_color,"skin":args.skin,
            "direction":args.direction,"seed":args.seed},indent=2),encoding="utf-8")
        print(f"Saved character: {out}")
    elif args.command=="animation":
        if args.frames<2: raise SystemExit("At least 2 frames are required.")
        make_animation(args)
    elif args.command=="autotile":
        make_autotile(args)


if __name__=="__main__":
    main()
