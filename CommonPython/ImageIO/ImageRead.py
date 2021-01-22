
import cv2
import numpy as np
import os

def read_image(fn, dtype=np.uint8):
    if ( not os.path.isfile(fn) ):
        raise Exception('%s does not exist. ' % (fn))

    return cv2.imread(fn, cv2.IMREAD_UNCHANGED).astype(dtype)
