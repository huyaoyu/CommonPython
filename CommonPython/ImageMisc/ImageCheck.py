from __future__ import print_function

import cv2
import numpy as np

def check_same_dimension(imgs):
    """
    imgs: A list-like. The images need to be checked.
    """

    # The number of images.
    N = len(imgs)

    if ( N <= 1 ):
        raise Exception("Only one image in the list.")

    # Check the value of dimensions.
    for i in range(1, N):
        for j in range(2):
            if ( imgs[0].shape[j] != imgs[i].shape[j] ):
                return False
    
    return True

def check_same_dimension_all(imgs):
    """
    imgs: A list-like. The images need to be checked.
    """

    # The number of images.
    N = len(imgs)

    if ( N <= 1 ):
        raise Exception("Only one image in the list.")

    # Check the number of dimensions
    n = len( imgs[0].shape )

    for i in range(1, N):
        if ( len( imgs[i].shape ) != n ):
            return False
        
    # Check the value of dimensions.
    for i in range(1, N):
        for j in range(n):
            if ( imgs[0].shape[j] != imgs[i].shape[j] ):
                return False
    
    return True
