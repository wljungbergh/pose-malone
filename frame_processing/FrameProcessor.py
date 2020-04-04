import numpy as np
from mtcnn import MTCNN

class FrameProcessor(MTCNN):
    def __init__(self):
        super().__init__()

    def most_confident_face(self, faces):
        confidences = [face['confidence'] for face in faces]
        return faces[np.argmax(confidences)]

    def get_box_coords(self, face):
        return face['box']

    def process_frame(self, frame):
        faces = self.detect_faces(frame)
        face = self.most_confident_face(faces)
        return self.get_box_coords(face)