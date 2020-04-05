import numpy as np
from cv2.dnn import readNetFromCaffe
from cv2.dnn import blobFromImage
from cv2 import resize

class CaffeProcessor():
    def __init__(self):
        self.proto_path = 'frame_processing/caffe_model/deploy.prototxt.txt'
        self.model_path = 'frame_processing/caffe_model/res10_300x300_ssd_iter_140000.caffemodel'
        self.detector = readNetFromCaffe(self.proto_path, self.model_path)

    def get_size_of_frame(self, frame):
        (self.h, self.w) = frame.shape[:2]

    def get_blob_from_frame(self, frame):
        return blobFromImage(resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False, crop=False)

    def most_confident_face(self, detections):
        confidences = [detections[0, 0, i, 2] for i in range(detections.shape[2])]
        box = detections[0, 0, np.argmax(confidences), 3:7] * np.array([self.w, self.h, self.w, self.h])
        return box.astype('int')

    def get_bbox(self, frame):
        self.get_size_of_frame(frame)
        blob = self.get_blob_from_frame(frame)
        self.detector.setInput(blob)
        detections = self.detector.forward()
        return self.most_confident_face(detections)

    def get_center(self, bbox):
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        return (int(round(bbox[0] + w/2)), int(round(bbox[1] + h/2)))

    def get_area(self, bbox):
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        return w*h

    def get_face(self, bbox, frame):
        x, y, x2, y2 = bbox
        return frame[y:y2, x:x2]