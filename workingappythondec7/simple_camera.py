import sys
import time
import cv2
import threading
from queue import Queue
from neweyes import *
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def parseImages(name, q1):
    cap = cv2.VideoCapture()
    cap.set(cv2.CAP_PROP_FPS, 60)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 0) # These options are spotty depending on your camera setup. On mac webcam this ain't working well.

    cap.open(0)


    if cap.isOpened():
        while q1.qsize() < 100:
            ret, frame = cap.read()
            if not q1.full():
                q1.put(frame)


def process(frame, prop):
    if prop > 0 and prop <= len(neweyes):
        frame = eval(neweyes[prop - 1])(frame)
    return frame


def processImages(name, q1, q2, prop):
    qformat = QImage.Format_RGBA8888
    # qformat = QImage.Format_RGB888
    while True:
        if q2.qsize() < 100 and not q2.full():  # This check might be useless since we pull from q2 so fast

            frame = q1.get()
            frame = process(frame, prop[0])
            propname = neweyes[(prop[0] - 1) % len(neweyes)]
            # print(propname)

            if frame.ndim == 3:
                cv2.putText(frame, propname, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (30, 220, 60), 2,
                            cv2.LINE_AA)
            else:
                # pass
                cv2.putText(frame, propname, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2,
                            cv2.LINE_AA)


            # frame = QtGui.QImage(frame.data, #Trying to display with QT
            #                    frame.shape[1],
            #                    frame.shape[0],
            #                    frame.strides[0],  # <--- +++
            #                    qformat)

            q2.put(frame)


def show_camera(imgQ):
    print('starting showThread')
    window_handle = cv2.namedWindow("USB Cam", cv2.WINDOW_NORMAL)
    fullscreen = False

    while imgQ.qsize() > 1:
        img = imgQ.get()

    while True:
        now = time.time()
        # s = imgQ.qsize()
        print(q1.qsize(), q2.qsize())
        # print(q.q.,.,size())

        img = imgQ.get()

        cv2.imshow("USB Cam", img)

        keyCode = cv2.waitKey(29) # Keeping it near 30 gives consistent frame times, going lower allows ~20 sometimes but also allows ~45
        # Stop the program on the ESC key
        if (keyCode & 0xFF) == 27:
            break
        # Allow shifting through the lenses
        elif keyCode == 44:
            prop[0] = (prop[0] - 1) % len(neweyes)
            print("using", neweyes[(prop[0]-1) % len(neweyes)])
        elif keyCode == 46:
            prop[0] = (prop[0] + 1) % len(neweyes)
            print("using", neweyes[(prop[0] - 1) % len(neweyes)])

        totTime = time.time() - now
        print(totTime*1000);
        if not fullscreen:  # For some reason, fullscreen doesn't work sometimes if you put it in the beginning of the function. Putting here fixes it
            cv2.setWindowProperty("USB Cam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            fullscreen = True
            print("running")

    cv2.destroyAllWindows()


if __name__ == "__main__":
    args = sys.argv

    q1 = Queue()
    q2 = Queue()
    quit = False

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
    time.sleep(1)
    show_camera(q2)







