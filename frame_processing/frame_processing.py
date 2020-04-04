import numpy as np
from mtcnn import MTCNN
from cv2.dnn import readNetFromCaffe
from cv2.dnn import blobFromImage
from cv2 import resize

class MTCNNProcessor(MTCNN):
    def __init__(self):
        super().__init__()

    def most_confident_face(self, faces):
        print(len(faces))
        confidences = [face['confidence'] for face in faces]
        if not confidences:
            face = []
        else:
            face = faces[np.argmax(confidences)]
            print(confidences)
        return face

    def get_box_coords(self, face):
        return face['box']

    def process_frame(self, frame):
        faces = self.detect_faces(frame)
        face = self.most_confident_face(faces)
        if not face:
            box_coords = []
        else:
            box_coords = self.get_box_coords(face)
        return box_coords


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

    def process_frame(self, frame):
        self.get_size_of_frame(frame)
        blob = self.get_blob_from_frame(frame)
        self.detector.setInput(blob)
        detections = self.detector.forward()
        return self.most_confident_face(detections)