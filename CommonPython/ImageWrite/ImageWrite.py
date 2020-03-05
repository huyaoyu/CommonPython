from __future__ import print_function

import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

# CommonPython package.
from CommonPython.Filesystem.Filesystem import get_filename_parts

def write_float_image_normalized(fn, img):
    """
    fn: The output filename.
    img: A single channel image.

    Only supports writing PNG image.
    """

    # Test the output directory.
    parts = get_filename_parts(fn)

    if ( not os.path.isdir(parts[0]) ):
        os.makedirs(parts[0])
    
    # Normalize img.
    img = img.astype(np.float32)
    img = img - img.min()
    img = img / img.max()
    img = np.clip(img * 255.0, 0.0, 255.0).astype(np.uint8)

    # Save the image.
    cv2.imwrite(fn, img, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    return img

def write_float_image_normalized_clip(fn, img, m0, m1):
    """
    fn: The output filename.
    img: A single channel image.
    m0, m1: the minimum and maximum value.

    Only supports writing PNG image.
    """

    if ( m0 >= m1 ):
        raise Exception("Wrong clipping bounds: {}, {}.".format(m0, m1))

    return write_float_image_normalized( fn, np.clip(img, m0, m1) ) 

def write_float_image_fixed_normalization(fn, img, m0, m1):
    """
    fn: The output filename.
    img: A single channel image.
    m0, m1: The lower and upper bounds. Values in img will be
    clipped by m0 an m1 before normalization.

    Only supports writing PNG image.
    """

    # Test the output directory.
    parts = get_filename_parts(fn)

    if ( not os.path.isdir(parts[0]) ):
        os.makedirs(parts[0])

    # Check the dimension of img.
    assert (img.ndim == 2), "img must be a 2D array img.shape = {}. ".format( img.shape )

    # Check the bounds.
    assert (m1 > m0), "m1 ({}) must larger than m0 ({}). ".format( m1, m0 )

    # Conver img to float type.
    img = img.astype(np.float32)

    # Clip the value.
    img = np.clip(img, m0, m1)

    # Normalization.
    img = (img - m0) / ( m1 - m0 )
    img = img * 255
    img = img.astype(np.uint8)

    # Save the image.
    cv2.imwrite(fn, img, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    return img

def write_float_image_plt(fn, img):
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(111)
    ax.axis("off")
    im = ax.imshow(img)
    fig.colorbar(im)
    fig.savefig(fn)
    plt.close(fig)

def write_float_image_plt_clip(fn, img, m0, m1):
    write_float_image_plt( fn, np.clip( img, m0, m1 ) )
    