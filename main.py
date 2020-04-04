import tensorflow as tf
import numpy as np

tf.logging.set_verbosity(tf.logging.ERROR)


from decision_making.decision_maker import DecisionMaker
from filtering.filter import Filter
from frame_capture.frame_capture import FrameCapturer
from headpose_estimator.headpose_estimator import HeadPoseEstimator
from frame_processing.frame_processing import CaffeProcessor
from notifier.notifier import MacOSNotifier

import time

from cv2 import FONT_HERSHEY_SIMPLEX
from cv2 import imread, imshow
from cv2 import rectangle, circle, putText
from cv2 import waitKey
from cv2 import destroyAllWindows


BLACK_SCREEN = np.ones((400,400,3))*int(255)







if __name__ == '__main__':
    
    t = time.time()
    # Initialize stuff
    t = time.time()
    print("Loading FrameCapturer ...")
    fc = FrameCapturer()
    print("Loading FrameProccessor ...")
    fp = CaffeProcessor()
    print("Loading HeadPoseEstimator ...")
    hpe = HeadPoseEstimator()
    print("Loading Filter ...")
    filt = Filter(100)
    print("Loading DecisionMaker ...")
    dm = DecisionMaker(100, 10, 10, 10, 50)
    print("Loading MacOSNotifier ...")
    notifier = MacOSNotifier()
    print(time.time() - t)


    # Initialize posture values 
    t = time.time() 
    init_counter = 0
    tot_centerX = 0
    tot_centerY = 0
    tot_area = 0
    tot_yaw = 0
    tot_pitch = 0
    tot_roll = 0

    while time.time() < t + 20:
        init_counter += 1
        print(init_counter)
        frame = fc.get_frame()
        frame_copy = frame.copy()

        bbox = fp.get_bbox(frame)
        face = fp.get_face(bbox, frame_copy)
        centerX, centerY = fp.get_center(bbox)
        tot_centerX += centerX
        tot_centerY += centerY
        tot_area += fp.get_area(bbox)
        (yaw, pitch, roll), _  = hpe.estimate_headpose(face)
        tot_pitch += pitch
        tot_roll += roll
        tot_yaw += yaw



    
    quit = False
    while (quit):

        frame = fc.get_frame()
        frame_copy = frame.copy()

        bbox = fp.get_bbox(frame)
        face = fp.get_face(bbox, frame_copy)
        center = fp.get_center(bbox)
        area = fp.get_area(bbox)

        x, y, x2, y2 = bbox
        rectangle(frame, (x, y), (x2, y2), (0,255,0), 1)
        circle(frame, center, 5, (0,255,0), 1)
        text = "Area = {}" .format(area)
        putText(frame, text, (x, y), FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        imshow('Frame', frame)
        print(face.shape[0], face.shape[1])
        if face.shape[0]>100 and face.shape[1]>100:
            p, img = hpe.estimate_headpose(face, render = True)
            imshow('Face', img)
            
        else:
            imshow('Face', BLACK_SCREEN)
        if waitKey(1) & 0xFF == ord('q'):
            break


    
print("DONE...")