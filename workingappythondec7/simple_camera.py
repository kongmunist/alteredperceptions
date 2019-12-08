import sys
import time
import cv2
import threading 
from queue import Queue
from neweyes import *


def parseImages(name, q1):
    cap = cv2.VideoCapture()
    cap.set(cv2.CAP_PROP_FPS, 60)

    cap.open(0)
    if cap.isOpened():
        while True:
            ret, frame = cap.read()
            
            if not q1.full(): 
                q1.put(frame)        

def process(frame, prop):

    if prop > 0 and prop <= len(neweyes):
        frame = eval(neweyes[prop-1])(frame)

    return frame 

def processImages(name, q1, q2, prop):
    while True:
        if not q2.full():
            frame = q1.get()
            q2.put(process(frame, prop))
    
        

        
        
        







def show_camera(imgQ):
    print('starting showThread')
    window_handle = cv2.namedWindow("USB Cam", cv2.WINDOW_NORMAL)
    #cv2.setWindowProperty("USB Cam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    fullscreen = False
    
    while imgQ.qsize() > 1:
        img = imgQ.get()

    # Window
    while True:
    
        now = time.time() 
        s = imgQ.qsize()

        #print(q.qsize())

        
        for i in range(s-1):
            imgQ.get()
        img = imgQ.get()
    

        cv2.imshow("USB Cam", img)

        keyCode = cv2.waitKey(15) & 0xFF
        # Stop the program on the ESC key
        if keyCode == 27:
            break
        totTime = time.time()-now
        #print(totTime*1000);
        if not fullscreen: # For some reason, fullscreen doesn't work sometimes if you put it in the beginning of the function. Putting here fixes it
            cv2.setWindowProperty("USB Cam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            fullscreen = True
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
    print("\tUsing " + neweyes[prop-1] + " eyes")
    
    
    t1 = threading.Thread(target = parseImages, args = ("parse", q1), daemon = True)
    t2 = threading.Thread(target= processImages, args = ("process", q1, q2, prop), daemon = True)

    t1.start()
    t2.start()
    time.sleep(3);
    show_camera(q2)






