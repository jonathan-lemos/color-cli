#!/usr/bin/python3

import argparse
import colorsys
import re


parser = argparse.ArgumentParser()

parser.add_argument("--asc",
                    dest="desc",
                    action="store_false",
                    default=False,
                    help="sort descending")

parser.add_argument("--desc",
                    dest="desc",
                    action="store_true",
                    help="sort descending")

parser.add_argument("--hue",
                    dest="type",
                    default="hue",
                    action="store_const",
                    const="hue",
                    help="sort by hue. this is the default")

parser.add_argument("--luminance",
                    dest="type",
                    action="store_const",
                    const="luminance",
                    help="sort by luminance")

parser.add_argument("--saturation",
                    dest="type",
                    action="store_const",
                    const="saturation",
                    help="sort by saturation")


def string_to_rgb(s):
    s = s.lstrip("#").upper()
    if not re.fullmatch(r"[0-9A-F]+", s):
        raise ValueError(f"'{s}' is not a valid hex color")
    if len(s) == 3:
        s = ''.join(c for pair in zip(s, s) for c in pair)
    if len(s) != 6:
        raise ValueError(f"'{s}' must have 3 or 6 hex digits")
    return tuple(int(''.join(pair), 16) for pair in zip(s[::2], s[1::2]))


args = parser.parse_args()
rgb_input = []
while True:
    try:
        rgb_input += [(x, string_to_rgb(x)) for x in input().strip().split()]
    except EOFError:
        break

rgb_hsl_input = [(x, rgb, colorsys.rgb_to_hsv(*rgb)) for x, rgb in rgb_input]
sorter = {
    "hue": lambda x: x[-1][0],
    "saturation": lambda x: x[-1][1],
    "luminance": lambda x: x[-1][2]
}
rgb_hsl_input = sorted(rgb_hsl_input, key=sorter[args.type], reverse=args.desc)
print("\n".join(x for x, _, _ in rgb_hsl_input))