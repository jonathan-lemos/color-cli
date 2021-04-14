#!/usr/bin/python3
import argparse
import cv2
import numpy as np


def color_to_rgb(a):
    r, g, b = (hex(round(n)).upper()[2:].ljust(2, '0') for n in a)
    return f"#{r}{g}{b}"


parser = argparse.ArgumentParser()

parser.add_argument("image",
                    metavar="image",
                    help="the image to compute the dominant color of")

parser.add_argument("count",
                    nargs="?",
                    metavar="count",
                    type=int,
                    default=5,
                    help="the amount of dominant colors to generate. default: 5")

args = parser.parse_args()

img = cv2.imread(args.image)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
average = img.mean(axis=0).mean(axis=0)

pixels = np.float32(img.reshape(-1, 3))
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
flags = cv2.KMEANS_RANDOM_CENTERS

_, labels, palette = cv2.kmeans(pixels, args.count, None, criteria, 10, flags)
_, counts = np.unique(labels, return_counts=True)

color_counts = sorted(zip(palette, counts), key=lambda x: x[1], reverse=True)
colors = [palette for palette, _count in color_counts]
color_codes = list(map(color_to_rgb, colors))

print("\n".join(color_codes))
