
import cv2
import matplotlib.pyplot as plt
import numpy as np

def show_image(img, name):
    fig = plt.figure(num=name)
    ax  = fig.add_subplot()
    if ( img.ndim == 2 or ( img.ndim == 3 and img.shape[2] == 1 )):
        ax.imshow( img, cmap='gray' )
    else:
        ax.imshow( img )
    plt.show()

    return fig