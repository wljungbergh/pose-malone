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
from math import sqrt

from cv2 import FONT_HERSHEY_SIMPLEX
from cv2 import imread, imshow
from cv2 import rectangle, circle, putText
from cv2 import waitKey
from cv2 import destroyAllWindows


BLACK_SCREEN = np.ones((400,400,3))*int(255)


def initialize_posture(fc: FrameCapturer, fp: CaffeProcessor, hpe: HeadPoseEstimator):
    # Initialize posture values 
    t = time.time() 
    init_counter = 0
    tot_centerX = 0
    tot_centerY = 0
    tot_area = 0
    tot_yaw = 0
    tot_pitch = 0
    tot_roll = 0

    while time.time() < t + 5:
        init_counter += 1.0
        
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

    pos = (tot_centerX/init_counter, tot_centerY/init_counter)
    area = tot_area/init_counter
    head_pose = np.array([tot_yaw/init_counter, tot_pitch/init_counter, tot_roll/init_counter])


    return pos, area, head_pose

if __name__ == '__main__':
    N = 2
    # Initialize stuff
    print("Loading FrameCapturer ...")
    fc = FrameCapturer()
    print("Loading FrameProccessor ...")
    fp = CaffeProcessor()
    print("Loading HeadPoseEstimator ...")
    hpe = HeadPoseEstimator()
    print("Loading Filters ...")
    pos_y_filter = Filter(N)
    area_filter = Filter(N)
    roll_filter = Filter(N)
    pitch_filter = Filter(N)
    
    
    print("Loading DecisionMaker ...")
    dm = DecisionMaker(10, 0.1, 0.1, 0.1, 5)
    print("Loading MacOSNotifier ...")
    notifier = MacOSNotifier()
    

    # Initialize posture    
    print("Starting initialize posture...")
    (posX, posY), area, head_pose = initialize_posture(fc, fp, hpe)
    print("Finished initialize posture...")
    # Set refrence posture accordingly
    print("posY ref: {}".format(posY))
    print("area ref: {}".format(area))
    print("head_pose ref: {}".format(head_pose))
    dm.set_references(sqrt(area), head_pose, posY)



    render = True
    quit = False
    while (not quit):

        frame = fc.get_frame()
        frame_copy = frame.copy()

        bbox = fp.get_bbox(frame)
        face = fp.get_face(bbox, frame_copy)
        center = fp.get_center(bbox)
        area = fp.get_area(bbox)
        area_filter.add_data(sqrt(area))
        print("ypos: {}".format(center[1]))
        pos_y_filter.add_data(center[1])
        # render if neccessary
        if render: 
            x, y, x2, y2 = bbox
            rectangle(frame, (x, y), (x2, y2), (0,255,0), 1)
            circle(frame, center, 5, (0,255,0), 1)
            text = "Area = {}" .format(area)
            putText(frame, text, (x, y), FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

            imshow('Frame', frame)
            
        if face.shape[0]>100 and face.shape[1]>100:
            (_, pitch, roll), img = hpe.estimate_headpose(face, render)
            pitch_filter.add_data(pitch)
            roll_filter.add_data(roll)
            if render:
                imshow('Face', face)
            
        else:
            if render:
                imshow('Face', BLACK_SCREEN)
        
        
        good_posture = dm.add_data(area_filter.get_smooth_data(), 0, pos_y_filter.get_smooth_data())
        print("Good posture? {}".format(good_posture))
        if not good_posture:
            notifier.send_notification(1, "Pose Malone Says")

        if waitKey(1) & 0xFF == ord('q'):
            break

    
print("DONE...")