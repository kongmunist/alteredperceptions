import numpy as np
import cv2 as cv
import time


def swap(im, ch1, ch2):
    one = im[:, :, ch1].copy()
    two = im[:, :, ch2].copy()
    im[:, :, ch1] = two
    im[:, :, ch2] = one

    return im

def draw_flow(img, flow, step=10):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    cv.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (_x2, _y2) in lines:
        cv.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis

cap = cv.VideoCapture(0)
i=0
flow = None
while(1):
    ret, frame = cap.read()



    # # "derivative", makes it look creepy as hell
    # kern = np.array([[0,0,0],[-5.0,0.0,5.0],[0,0,0]])
    # frame = cv.filter2D(frame,-1, kern)

    # # Median, looks funky and color-palettizes the image but is so slow probably cause it has to max over a lot of pixels
    # frame = cv.medianBlur(frame, 51)

    # # Looks normal blurry
    # frame = cv.bilateralFilter(frame, 9, 500,500)

    # # does interesting things to the eyes... can apply multiple times using optional params (iterations = 2)
    # kern = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
    # # kern = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    # # frame = cv.dilate(frame, kern) # Weird squinty eyes
    # frame = cv.erode(frame, kern,iterations=2) # Anime eyes

    # kern = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11, 11))
    # frame = cv.erode(frame, kern) # BIG anime eyes

    # # Makes thin things disappear
    # kern = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11, 11))
    # frame = cv.morphologyEx(frame, cv.MORPH_OPEN, kern)

    # # Very funky looking - blackens and makes edges emphasized
    # kern = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    # frame = cv.morphologyEx(frame, cv.MORPH_GRADIENT, kern)

    # # keeps White things only, very unsettling to look at eyes
    # kern = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11,11))
    # frame = cv.morphologyEx(frame, cv.MORPH_TOPHAT, kern)
    # frame = cv.morphologyEx(frame, cv.MORPH_BLACKHAT, kern)

    # # Very noir-like
    # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # # cv.medianBlur(frame, 5)
    # _, frame = cv.threshold(frame, 100, 255, cv.THRESH_BINARY)

    # # Adaptive thresholding, looks really strange but could be cool. Can blur before or after
    # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # # frame = cv.adaptiveThreshold(frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 3, 2)
    # frame = cv.adaptiveThreshold(frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2) # Changing last value higher makes lighter, but weird ,changing second to last value makes lines stronger
    # # cv.GaussianBlur(frame, (5, 5), -1)
    # # cv.medianBlur(frame, 3)

    # # Color channels swap. Really weird looking, but pretty mundane
    # frame = swap(frame, 0,2)

    # # Take a color channel as the greyscale values. Could do something interesting by adding/subtracting different channels after thresholding?
    # frame = frame[:,:,2]

    # Select only one channel to see - preserves color so everything is red tinted
    # min = 50
    # frame[:, :, 0] = frame[:,:,0]
    # frame[:, :, 1] = 50
    # frame[:, :, 2] = 50

    # # Use normal canny for edges
    # frame = cv.Canny(frame, 100, 200)



    # # Optical Flow  # Achieving 200 ms latency. Better than starting but still too slow
    # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # try:
    #     now = time.time()
    #
    #     flow = cv.calcOpticalFlowFarneback(prev, frame, None, .5, 2, 15, 1,
    #                                            5, 1.2, 0)
    #
    #
    #     flowMag = (flow[:, :, 0] ** 2 + flow[:, :, 1] ** 2) ** .5
    #     flowMag = flowMag / np.max(flowMag) #* 255.0
    #     frame = np.multiply(frame, flowMag)
    #
    #     print(time.time() - now)
    # except:
    #     prev=frame



    # # Implement Laplacian
    # sur = -1
    # kern = np.array([[sur, sur, sur], [sur, 8, sur], [sur, sur, sur]])
    # frame = cv.filter2D(frame, -1, kern)


    # Implement broken Laplacian which overwrites itself
    # frame = cv.resize(frame, (0,0),fx=.25,fy=.25)
    # sur = -1
    # kern = np.array([[sur, sur, sur], [sur, 8, sur], [sur,sur,sur]])
    # for i in range(1,len(frame)-2):
    #     for j in range(1,len(frame[0])-2):
    #
    #         frame[i][j] *= 9
    #         r = sum(sum(frame[i-1:i+2,j-1:j+2,0]))
    #         g = sum(sum(frame[i - 1:i + 2, j - 1:j + 2, 1]))
    #         b = sum(sum(frame[i - 1:i + 2, j - 1:j + 2, 2]))
    #
    #         yea = -1*(np.array([r,g,b]))
    #         yea = np.clip(yea, 0,255)#.astype('int8')
    #         frame[i][j] = yea



    # frame = cv.filter2D(frame, -1, kern)







    # mask = np.zeros(frame.shape[:2], np.uint8)
    #
    # bgdModel = np.zeros((1, 65), np.float64)
    # fgdModel = np.zeros((1, 65), np.float64)
    # rect = (0, 0, len(frame[0]), len(frame))
    # frame = cv.grabCut(frame, mask,rect, bgdModel, fgdModel, 5)
    #
    # mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    # frame = frame * mask2[:, :, np.newaxis]

    # frame = cv.Laplacian(frame, 3, frame, 1)



    # frame = cv.erode(frame, cv.getStructuringElement(3, cv.Size(5,5)))

    # frame = cv.Laplacian(frame, 1)

    # ret, thresh1 = cv.threshold(imgray, 127, 255, 0)
    # im = frame*[[1.0,3.0,1.0]]
    # im = frame
    # im = frame*[[[.5],[0.5],[.5]],[[0.0],[0.0],[0.0]],[[-.5],[-0.5],[-.5]]]
    # im = frame*[[.5,0.5,.5],[0.0,0.0,0.0],[-.5,-0.5,-.5]]





    # imgray.sort()
    # im = imgray

    cv.imshow('frame',frame)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()


# # Rectangular Kernel
# >>> cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
# array([[1, 1, 1, 1, 1],
#        [1, 1, 1, 1, 1],
#        [1, 1, 1, 1, 1],
#        [1, 1, 1, 1, 1],
#        [1, 1, 1, 1, 1]], dtype=uint8)
#
# # Elliptical Kernel
# >>> cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
# array([[0, 0, 1, 0, 0],
#        [1, 1, 1, 1, 1],
#        [1, 1, 1, 1, 1],
#        [1, 1, 1, 1, 1],
#        [0, 0, 1, 0, 0]], dtype=uint8)
#
# # Cross-shaped Kernel
# >>> cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))
# array([[0, 0, 1, 0, 0],
#        [0, 0, 1, 0, 0],
#        [1, 1, 1, 1, 1],
#        [0, 0, 1, 0, 0],
#        [0, 0, 1, 0, 0]], dtype=uint8)