import cv2

def blur_resize(img, factor, kenerlSize=(5, 5)):
    imgG = cv2.GaussianBlur( img, kenerlSize, 0 )
    return cv2.resize(imgG, (0, 0), fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)