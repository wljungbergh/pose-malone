import sys, os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'frame_capture')))
print(sys.path)

from cv2 import imread
from cv2 import imshow
from cv2 import rectangle
from cv2 import waitKey
from cv2 import destroyAllWindows
from mtcnn import MTCNN
from frame_processing import MTCNNProcessor
from frame_processing import CaffeProcessor
from frame_capture import FrameCapturer


capturer = FrameCapturer()
detector = CaffeProcessor()

while True:
    frame = capturer.get_frame()
    face = detector.process_frame(frame)

    x, y, x2, y2 = face
    rectangle(frame, (x, y), (x2, y2), (0,255,0), 1)

    imshow('hej', frame)
    if waitKey(1) & 0xFF == ord('q'):
        break

destroyAllWindows()
