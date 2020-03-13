#!/usr/local/bin/python3
import argparse
import json
import sys
from histo import Histo
from PIL import Image

parser = argparse.ArgumentParser(prog="SecHPlot", description="Plot secured histogram of an image.")
parser.add_argument("-r", "--ref_points", nargs=1, type=argparse.FileType('r'), required=True, help="Filepath for the points of reference (json format)")
parser.add_argument("-i", "--image", nargs=1, type=argparse.FileType('r'), required=True, help="Filepath of the image to compute (json or png)")
parser.add_argument("-j", "--json", action="store_true", help="Need this options if using a json for the image")

if __name__ == "__main__":
    args = parser.parse_args()
    dec = json.JSONDecoder()
    ref = dec.decode(args.ref_points[0].read())    
    if args.json:
        data = dec.decode(args.image[0].read())
    else:
        image = Image.open(args.image[0].name)
        # Y = 0.2125 R + 0.7154 G + 0.0721 B
        data = list(image.convert("LA").getdata())

    hist = Histo(ref, data)
    hist.plot_unsecure()    
