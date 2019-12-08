import cv2
import numpy as np

                    # Kernel and Convolution-based eyes

kernRect = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
kernEllipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
kernCross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))

kernBigEllipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))

kernDerivative = np.array([[0, 0, 0], [-5.0, 0.0, 5.0], [0, 0, 0]])
# kernDerivative = np.array([[0, -5, 0], [-5.0, 0.0, 5.0], [0, 5, 0]])

# backSub = cv2.createBackgroundSubtractorKNN() # Default is good, but edited is faster
# backSub = cv2.createBackgroundSubtractorKNN(history=3, detectShadows=False)
backSub = cv2.createBackgroundSubtractorMOG2(history=10, detectShadows=False)

class ghostly():
    def __init__(self, gamma):
        self.initialized = False
        self.gamma = gamma

    def apply(self, frame):
        if not self.initialized:
            self.prev = np.copy(frame)
            self.initialized = True
            return frame
        else:
            frame = frame*(1-self.gamma) + self.prev*self.gamma
            frame = frame.astype(np.uint8)

            self.prev = np.copy(frame)
            return frame

ghostFilter = ghostly(.96) #Goes exponential





# Convert to grayscale image
def apGrayscale(frame):

    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Canny edge detection
def apCanny(frame, t1 = 90, t2 = 180):
    frame = apGrayscale(frame)
    return cv2.Canny(frame, t1, t2)

# Finds edges and adds color from original image
def apColorEdges(frame):
    mask = apCanny(frame)
    return cv2.bitwise_and(frame, frame, mask=mask)

# Similar to previous, but makes the space bigger first
def apNovelInfo(frame):
    mask = apCanny(frame)
    mask = apGaussian(mask)
    mask = apGaussian(mask)
    return cv2.bitwise_and(frame, frame, mask=mask)


# Dilate and Erode, makes eyes look weird
def apErosion(frame, iters=1, kernel = kernEllipse):
    return cv2.erode(frame, kernel, iterations=iters)
    
def apDilate(frame, iters=1, kernel = kernEllipse):
    return cv2.dilate(frame, kernel, iterations=iters)

# standard Gaussian blur
def apGaussian(frame, kSize=5):
    return cv2.GaussianBlur(frame, (kSize,kSize), -1)

# "derivative", makes it look creepy as hell
def apDerivative(frame):
    return cv2.filter2D(frame,-1, kernDerivative)

# Median blur
def apMedian(frame, ksize=5):
    return cv2.medianBlur(frame, ksize)

# BIG anime eyes
def apBigErode(frame):
    return cv2.erode(frame, kernBigEllipse)

# Makes thin things disappear
def apOpen(frame):
    return cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernBigEllipse)

# Very funky looking - blackens and makes edges emphasized
def apGradient(frame):
    return cv2.morphologyEx(frame, cv2.MORPH_GRADIENT, kernBigEllipse)

# keeps White things only, very unsettling to look at eyes
def apHatFilter(frame):
    return cv2.morphologyEx(frame, cv2.MORPH_BLACKHAT, kernBigEllipse)
    # return cv2.morphologyEx(frame, cv2.MORPH_TOPHAT, kernBigEllipse)

def apLaplacian(frame, surroundings=-1):
    kern = np.ones((3, 3)) * surroundings
    kern[1][1] = 8
    return cv2.filter2D(frame, -1, kern)

                        # Video/Multi-frame eyes


# Adaptive thresholding, looks really strange but could be cool. Can blur before or after
def apAdaptiveThresh(frame):
    frame = apGrayscale(frame)
    frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2) # Changing last value higher makes lighter, but weird ,changing second to last value makes lines stronger
    # # cv2.GaussianBlur(frame, (5, 5), -1)
    # # cv2.medianBlur(frame, 3)
    return frame

def apBackgroundSubtraction(frame):
    frame = backSub.apply(frame)
    return frame # Try editing the frame, dilate or erode or something else

def apGhostly(frame):
    return ghostFilter.apply(frame)

                        # Channel editing eyes

# Color channels swap. Really weird looking, but pretty mundane
def apChannelSwap(frame, ch1 = 0, ch2 = 2):
    one = frame[:, :, ch1].copy()
    two = frame[:, :, ch2].copy()
    frame[:, :, ch1] = two
    frame[:, :, ch2] = one
    return frame

# Take a color channel as the greyscale values. Could do something interesting by adding/subtracting different channels after thresholding?
def apOneChannelAsGreyscale(frame, ch1 = 1):
    return frame[:,:,2]

# Select only one channel to see - preserves color so everything is red tinted
def apOneChannelAsColor(frame, ch1 = 1, min = 80):
    frame[:, :, ch1] = frame[:,:,ch1]
    for i in range(3):
        if i != ch1:
            frame[:,:,i] = min
    return frame
