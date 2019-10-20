from __future__ import print_function

import argparse
import cv2
import numpy as np
import os

def get_filename_parts(fn):
    p = os.path.split(fn)

    f = os.path.splitext(p[1])

    return [ p[0], f[0], f[1] ]

if __name__ == "__main__":
    print("Denoise an image.")

    parser = argparse.ArgumentParser(description="Denoise an image.")

    parser.add_argument("infile", type=str, \
        help="The input file.")
    parser.add_argument("outfile", type=str, \
        help="The output file.")
    parser.add_argument("--w-luminance", type=float, default=3.0, \
        help="The window size of color luminance filter.")
    parser.add_argument("--w-color", type=float, default=3.0, \
        help="The window size of color filter.")
    
    args = parser.parse_args()

    # Open the input file.
    img = cv2.imread(args.infile, cv2.IMREAD_UNCHANGED)

    # Test the output directory.
    parts = get_filename_parts(args.outfile)

    if ( not os.path.isdir( parts[0] ) ):
        os.makedirs( parts[0] )

    # Denoise.
    if ( 3 == len( img.shape ) ):
        dst = cv2.fastNlMeansDenoisingColored( img, h=args.w_luminance, hColor=args.w_color )
    elif ( 1 == len( img.shape ) ):
        dst = cv2.fastNlMeansDenoising( img, h=args.w_luminance )
    else:
        raise Exception("len( img.shape ) == %d." % ( len( img.shape ) ))

    # Save the image.
    cv2.imwrite(args.outfile, dst, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    print("Denoised image is saved to %s." % ( args.outfile ))
    print("Done.")
