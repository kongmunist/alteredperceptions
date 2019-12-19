import cv2
import math
import numpy as np
from rejectedeyes import *
                    # Kernel and Convolution-based eyes

# Chose (3,3) for more iterations cause it's way faster than 5x5 for 1
kernRect = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
kernEllipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
kernCross = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))

kernBigEllipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))

# Top one makes left edges white, bottom makes x=y line white
#kernDerivative = np.array([[0, 0, 0], [-5.0, 0.0, 5.0], [0, 0, 0]])
kernDerivative = np.array([[0, -5, 0], [-5.0, 0.0, 5.0], [0, 5, 0]])

backSub = cv2.createBackgroundSubtractorMOG2(history=10, detectShadows=False)

class ghostly():
    def __init__(self, gamma, gamma2 = -2):
        self.initialized = False
        if gamma2 == -2:
            self.gamma2 = 1-gamma
        else:
            self.gamma2 = gamma2

        self.gamma = gamma

    def apply(self, frame):
        if not self.initialized:
            self.prev = np.copy(frame)
            self.initialized = True
            return frame
        else:
            frame = frame*self.gamma2 + self.prev*self.gamma
            frame = frame.astype(np.uint8)

            self.prev = np.copy(frame)
            return frame



ghostFilter = ghostly(.96) #Goes exponential
ghostForBacksub = ghostly(.7)
ghostForSubtraction = ghostly(1,-1)
prev = [3]

def apNoOp(frame):
    prev[0] = 0
    return frame

def apInvert(frame):
    return 255-frame


# Interesting movement effects, but too noisy to use. Get rid of high frequency noise and we can talk
def apSubtract(frame): 
    # frame = ghostForSubtraction.apply(frame)
    # return frame
    try:
        tmp = prev[0].copy() - frame.copy() 
    except:
        tmp = frame
    prev[0] = frame
    return tmp-128

# Convert to grayscale image
def apGrayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Finds edges and adds color from original image
def apColorEdges(frame):
    mask = apCanny(frame)
    return cv2.bitwise_and(frame, frame, mask=mask)

# Dilate and Erode, makes eyes look weird
def apErosion(frame, iters=2, kernel = kernEllipse):
    return cv2.erode(frame, kernel, iterations=iters)
    
def apDilate(frame, iters=1, kernel = kernEllipse):
    return cv2.dilate(frame, kernel, iterations=iters)

# "derivative", makes it look creepy as hell
def apDerivative(frame):
    #frame = apGrayscale(frame)
    return cv2.filter2D(frame,-1, kernDerivative)


                        # Video/Multi-frame eyes

# Adaptive thresholding, looks really strange but could be cool. Can blur before or after
def apAdaptiveThresh(frame):
    frame = apGrayscale(frame)
    frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2) # Changing last value higher makes lighter, but weird ,changing second to last value makes lines stronger
    # # cv2.GaussianBlur(frame, (5, 5), -1)
    # # cv2.medianBlur(frame, 3)
    return frame

def apBackgroundSubtraction(frame):
    tmp = frame.copy()
    # frame = apLaplacian(frame) # TERROR
    frame = backSub.apply(frame)
    frame = cv2.medianBlur(frame, 3)
    frame = ghostForBacksub.apply(frame)

    # frame = cv2.bitwise_and(tmp,tmp, mask=frame)
    #frame = apLaplacian(frame)
    return frame # Try editing the frame, dilate or erode or something else

                        # Channel editing eyes

# Color channels swap. Really weird looking, but pretty mundane
def apChannelSwap(frame, ch1 = 0, ch2 = 2):
    one = frame[:, :, ch1].copy()
    two = frame[:, :, ch2].copy()
    frame[:, :, ch1] = two
    frame[:, :, ch2] = one
    return frame

scale = .8
itera = .08
rgbfactor = np.array([0,scale*2,scale*2])
iters = np.array([itera, itera, -itera])

class rainbow():
    def __init__(self, scale, iters):
        self.scale = scale
        self.iters = iters
        self.rgbfactor = np.array([0,scale*2, scale*2])
        self. iterfactor = np.array([iters, iters, -iters])
    def apply(self, frame):
        for i in range(3):
            if self.rgbfactor[i] > self.scale*2 or self.rgbfactor[i] < 0:
                self.iterfactor[i] = -self.iterfactor[i]
        self.rgbfactor += self.iterfactor

        self.rgbfactor = np.array([[1],[1],[1]])
        frame = np.multiply(frame, self.rgbfactor)
        print(self.rgbfactor)
        return frame

rainbowCycle = rainbow(0.4, .08)
def apRainbow(frame):
    frame = rainbowCycle.apply(frame) 
    return frame

def apLinearResize(frame,scale = .15):
    frame = cv2.resize(frame,(0,0),fx=scale,fy=scale)  # 2nd resize is for name to not be super big in corner
    frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_NEAREST)

    return frame

#def apResize(frame, x=.15,y=.15,cycNum = [0.3,.5],inter = cv2.INTER_NEAREST):
def apResize(frame, x=.08,y=.08,cycNum = [0,.05],inter = cv2.INTER_AREA):
    #frame = apMedian(frame)
    if cycNum[0] >= 4 or cycNum[0] < .3:
        cycNum[1] = -cycNum[1]

    #quant = 10
    #cyc=[(0,0),(quant,0),(quant,quant),(0,quant)] 
    #sel = cyc[cycNum[0]+1]
    cycNum[0] = (cycNum[0] + cycNum[1])
    numer = cycNum[0]
    #print(cycNum,numer)
    divider = 10
    frame = cv2.resize(frame,(0,0),fx= (1+numer/divider), fy=(1+numer/divider))

    frame = cv2.resize(frame,(0,0), fx=x,fy=y)
    #frame = cv2.resize(frame[sel[0]:(480-sel[0]),sel[1]:(640-sel[1])],(0,0), fx=x,fy=y)
    frame = cv2.resize(frame,(640,480), interpolation=inter)
    #frame = cv2.resize(frame[cyc[0]:(640-cyc[0]),cyc[1]:(480-cyc[1])],(640,480), interpolation=inter)
    return frame


def aLINEAR(frame):
    return apResize(frame, inter = cv2.INTER_LINEAR)

def aLAZLO(frame):
    return apResize(frame, inter = cv2.INTER_LANCZOS4)






