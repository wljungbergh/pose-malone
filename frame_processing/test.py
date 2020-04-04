import sys, os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'frame_capture')))
print(sys.path)
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'headpose_estimator')))
import headpose_estimator

from cv2 import FONT_HERSHEY_SIMPLEX
from cv2 import imread
from cv2 import imshow
from cv2 import rectangle, circle, putText
from cv2 import waitKey
from cv2 import destroyAllWindows
from mtcnn import MTCNN
from frame_processing import MTCNNProcessor
from frame_processing import CaffeProcessor
from frame_capture import FrameCapturer
import numpy as np


capturer = FrameCapturer()
detector = CaffeProcessor()
hp = headpose_estimator.HeadPoseEstimator()
black_screen = np.ones((400,400,3))*int(255)

while True:
    frame = capturer.get_frame()
    frame_copy = frame.copy()

    bbox = detector.get_bbox(frame)
    face = detector.get_face(bbox, frame_copy)
    center = detector.get_center(bbox)
    area = detector.get_area(bbox)

    x, y, x2, y2 = bbox
    rectangle(frame, (x, y), (x2, y2), (0,255,0), 1)
    circle(frame, center, 5, (0,255,0), 1)
    text = "Area = {}" .format(area)
    putText(frame, text, (x, y), FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    imshow('Frame', frame)
    print(face.shape[0], face.shape[1])
    if face.shape[0]>100 and face.shape[1]>100:
        p, img = hp.estimate_headpose(face, render = True)
        imshow('Face', img)
        
    else:
        imshow('Face', black_screen)
    if waitKey(1) & 0xFF == ord('q'):
        break

destroyAllWindows()
