from PIL import Image, ImageOps
import numpy as np
import argparse
from sys import argv


def image_filter(pixels: np.array, imgsize, x, y, delta, r=11, superp=0):
    red, gre, blu = 0, 0, 0
    rsq = r ** 2 - 1
    c = r // 2
    out = pixels[x - r // 2:x + c % imgsize[0], y - r // 2: y + c % imgsize[1]]
    red, gre, blue = out.sum((1, 0))
    if superp:
        return tuple(map(lambda col: superp - abs(int((delta + col / rsq) % 255)), (red, gre, blu)))
    return tuple(
        map(lambda col: abs(int((delta + col / rsq) % 255)), (red, gre, blu)))


def filt(image, delta, r, superp, invert):
    delta, r, superp, invert = map(lambda x: x[0] if type(x) == list else x, (delta, r, superp, invert))
    px = np.array(image)
    size = px.shape
    for i in range(0, size[0]):  # width
        for j in range(0, size[1]):  # height
            px[i, j] = image_filter(px, size, i, j, delta=delta, r=r,
                                    superp=superp)
    img = Image.fromarray(px)
    if invert:
        img = ImageOps.invert(img)
    return img


def img_conv(name: str):
    return Image.open(name).convert("RGB")


s = ''
parser = argparse.ArgumentParser()
parser.add_argument("Delta", type=int, nargs=1, metavar="D")
parser.add_argument("Radius", type=int, nargs=1, metavar="R")
parser.add_argument("MinusParam", type=int, nargs="?", metavar="P", default=0)
parser.add_argument("--invert", type=bool, nargs="?", metavar="T", default=False, const=True)
parser.add_argument("--name", type=str, nargs="?", metavar="I", default="in.jpg")
parser.add_argument("--out", type=str, nargs="?", metavar="O", default="out.jpg")
if __name__ == "__main__":
    if s := argv[1:]:
        args = parser.parse_args(s)
        filt(
            img_conv(args.name),
            args.Delta,
            args.Radius,
            args.MinusParam,
            args.invert).save(args.out)
    else:
        while (s := input()) != "":
            args = parser.parse_args(s.split())
            filt(
                img_conv(args.name),
                args.Delta,
                args.Radius,
                args.MinusParam,
                args.invert).save(args.out)
    # i = 1
    # for invert in (False, True):
    #     for r in range(2, 15):
    #         for delta in range(0, 255, 5):
    #             for minus in range(0, 255, 30):
    #                 print(f"Now: {i}.{delta}_{r}_{minus}_{invert}.jpg")
    #                 filt(
    #                     Image.open("in.jpg"),
    #                     delta,
    #                     r,
    #                     minus,
    #                     invert).save(f"{i}.{delta}_{r}_{minus}_{invert}.jpg")
    #                 i += 1
    #                 print("Done!")