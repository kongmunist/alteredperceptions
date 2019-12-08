import cv2
import numpy as np

kernRect = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
kernEllipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
kernCross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))

def apGrayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def apCanny(frame):
    frame = apGrayscale(frame)
    return cv2.Canny(frame, 90,180)

def apColorEdges(frame):
    mask = apCanny(frame)
    return cv2.bitwise_and(frame, frame, mask=mask)

def apNovelInfo(frame):
    mask = apCanny(frame)
    mask = apGaussian(mask) 
    mask = apGaussian(mask) 
    return cv2.bitwise_and(frame, frame, mask=mask)

def apErosion(frame):
    return cv2.erode(frame, kernRect)
    
def apDilate(frame):
    return cv2.dilate(frame, kernRect)

def apGaussian(frame):
    return cv2.GaussianBlur(frame, (5,5), -1)
