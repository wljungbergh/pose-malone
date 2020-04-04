from cv2 import imread
from cv2 import imshow
from cv2 import rectangle
from cv2 import waitKey
from cv2 import destroyAllWindows
from mtcnn import MTCNN
from FrameProcessor import FrameProcessor


pixels = imread('FrameProcessing/test_img.jpg')
print('Img shape: ', pixels.shape)

classifier = FrameProcessor()
x, y, w, h = classifier.process_frame(pixels)

x2, y2 = x + w, y + h
rectangle(pixels, (x, y), (x2, y2), (0,255,0), 1)


imshow('hej', pixels)
waitKey(0)
destroyAllWindows()
