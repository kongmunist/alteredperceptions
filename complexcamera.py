import sys
import time
import cv2
import threading
from queue import Queue
from neweyes import *
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def parseImages(name, q1):
    cap = cv2.VideoCapture()
    cap.set(cv2.CAP_PROP_FPS, 60)
    cap.open(0)
    frameSize[0] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frameSize[1] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    if cap.isOpened():
        while True:
            ret, frame = cap.read()
            q1[0] = frame




def process(frame, prop,lim):
    if prop >= 0 and prop <= lim:
        frame = eval(neweyes[(prop - 1) % lim])(frame)
    return frame


def processImages(name, q1, q2, prop):
    lim = len(neweyes)

    while type(q1[0]) == int:
        time.sleep(.1)

    while True:
        frame = q1[0].copy()

        frame = process(frame, prop[0],lim)

        propname = neweyes[(prop[0] - 1) % lim]
        # print(propname)

        try:
            if frame.ndim == 3:
                frame = cv2.putText(frame.copy(), propname, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (30, 220, 60), 2,
                            cv2.LINE_AA)
            else:
                frame = cv2.putText(frame.copy(), propname, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2,
                        cv2.LINE_AA)
        except:
            pass

        q2[0] = frame

class Window(QWidget):
    def __init__(self, imgQ, parent = None):
        QWidget.__init__(self, parent)
        self.imgQ = imgQ
        self.viewer = QLabel()
        self.timer = QTimer()
        self.timer.timeout.connect(self.makePicture)
        self.timer.start(10)


        self.viewer.setWindowFlag(Qt.Window)
        self.viewer.showFullScreen()
        # self.setWindowTitle(self.tr("Simple Threading Example"))

    def makePicture(self):
        now = time.time()
        # for i in range(self.imgQ.qsize()-1):
        #     self.imgQ.get()
        img = self.imgQ.get()
        print((time.time() - now) * 1000)
        print()
        # img = cv2.resize(img, (1440,960))

        # print((time.time() - now) * 1000)
        # now = time.time()
        # Convert opencv image to pixmap
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        #qImg = QImage(img.data, frameSize[1], frameSize[0], #bytesPerLine,
        qImg = QImage(img.data, 1440, 960, bytesPerLine, # Probably should make this more dynamic
                            QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(qImg)




        self.viewer.setPixmap(pixmap)
        self.viewer.repaint()



def show_camera(imgQ):
    print('starting showThread')
    window_handle = cv2.namedWindow("USB Cam", cv2.WINDOW_NORMAL)
    fullscreen = False

    checksum = 0

    while True:
        now = time.time()
        img = imgQ[0].copy()

        tmpValue = img[:5,:5].sum()

        if tmpValue != 9600 and (checksum != tmpValue or checksum == 0):
            checksum = tmpValue
            cv2.imshow("USB Cam", img)

            keyCode = cv2.waitKey(1)
            # Stop the program on the ESC key
            if (keyCode & 0xFF) == 27:
                break
            elif keyCode == 44:
                prop[0] = (prop[0] - 1) % len(neweyes)
                print("using", neweyes[(prop[0]-1) % len(neweyes)])
            elif keyCode == 46:
                prop[0] = (prop[0] + 1) % len(neweyes)
                print("using", neweyes[(prop[0] - 1) % len(neweyes)])


            totTime = time.time() - now
            print(totTime*1000)

            if not fullscreen:
                # For some reason, fullscreen doesn't work sometimes if you put it in the beginning of the function. Putting here fixes it
                cv2.setWindowProperty("USB Cam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                fullscreen = True
                print("running with screen size ", end = "")
                print(frameSize)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    args = sys.argv

    # q1 = Queue()
    # q2 = Queue()
    q1=[1]
    q2=[2]

    quit = False
    frameSize = [0,0]

    neweyes = open('neweyes.py', 'r').read().split("\n")
    neweyes = [x[4:x.index("(")] for x in neweyes if x[0:3] == "def"]

    try:
        prop = int(args[1])
    except:
        prop = 1
    print("\tUsing " + neweyes[prop - 1] + " eyes")
    prop = [prop]

    t1 = threading.Thread(target=parseImages, args=("parse", q1), daemon=True)
    t2 = threading.Thread(target=processImages, args=("process", q1, q2, prop),
                          daemon=True)



    t1.start()
    t2.start()
    # makeQT()

    time.sleep(1)
    show_camera(q2)


# Weird behavior: declaring a variable in the "run if main" function allows you
# to access it in any of the threads without sending it there.
# This also allows you to access it in the show_camera main function. Wack!





