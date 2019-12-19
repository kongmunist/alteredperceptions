import cv2
import numpy as np


#                       These 4 are too slow
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
    # return cv2.morphologyEx(frame, cv2.MORPH_TOPHAT, kernBigEllipse):wq



# failed laplacian, too slow
kern = np.ones((3, 3)) * -1
kern[1][1] = 8 
#return cv2.filter2D(frame, -1, kern)


# Both blurs are too boring
# Median blur
def apMedian(frame, ksize=5):
    frame = cv2.medianBlur(frame, ksize)
    return cv2.medianBlur(frame, ksize)

# standard Gaussian blur
def apGaussian(frame, kSize=5):
    return cv2.GaussianBlur(frame, (kSize,kSize), -1)

# Less optimal background subtractions
# backSub = cv2.createBackgroundSubtractorKNN() # Default is good, but edited is faster
# backSub = cv2.createBackgroundSubtractorKNN(history=3, detectShadows=False)

# janky shit, ugly and boring.
def apSharpenLaplacian(frame):
    frame = apGrayscale(frame)
    #frame = cv2.boxFilter(frame,-1,ksize=(5,5))
    return frame-apGaussian(apLaplacian(frame)*apCanny(frame))

# Not cool enough, but might be included anyway
def apCanny(frame, th1 = 80, th2 = 200):
    frame = cv2.Canny(frame, th1, th2)
    return frame


#Not cool enough compared to colorededges
# Similar to previous, but makes the space bigger first
def apNovelInfo(frame):
    mask = apCanny(frame)
    mask = apGaussian(mask)
    mask = apGaussian(mask)
    return cv2.bitwise_and(frame, frame, mask=mask)

def apScharrX(frame):
    return cv2.Scharr(frame, -1, 1,0)

def apScharrY(frame):
    return cv2.Scharr(frame, -1, 0,1)

# Too noisy to use
# you tried to do it yourself but it was too slow
def apLaplacian(frame, surroundings=-1):
    return cv2.Laplacian(frame,-1,ksize=5)

# Too strong of a ghostly lag to use, but hana said it most resembles drugs
def apGhostly(frame):
    return ghostFilter.apply(frame)

# Not cool enough
# Select only one channel to see - preserves color so everything is red tinted
def apOneChanCol(frame, ch1 = 2, minimum = .5):
    if len(channels) == 3:
        channels.remove(ch1)
    for thing in channels:
        frame[:,:,thing] = frame[:,:,thing]*minimum
    return frame
channels = [0,1,2]

# Not cool enough
# Take a color channel as the greyscale values. Could do something interesting by adding/subtracting different channels after thresholding?
def apOneChannelAsGreyscale(frame, ch1 = 1):
    return frame[:,:,2]


# Interesting movement effects, but too noisy to use. Get rid of high frequency noise and we can talk
def apSubtract(frame):
    # frame = ghostForSubtraction.apply(frame)
    # return frame
    try:
        tmp = frame.copy() - prev[0].copy()
    except:
        tmp = frame
    prev[0] = frame
    return tmp

# Gross looking but cool
def apScaleDown(frame):
    frame = frame-50
    return frame

# Tried to make a filter that made everything move slowly, by resizing bigger and smaller. Worked to make an aliased variable in the function, and did some slow stuff with the world. Should target a breathing frequency with sine wave.
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

def aCUBIC(frame):
    return apResize(frame, inter = cv2.INTER_CUBIC)


