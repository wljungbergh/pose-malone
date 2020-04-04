import os
import time
import numpy as np

class Decision_maker:

    def __init__(self, samples_to_keep, distance_tolerance, head_angle_tolerance, face_height_tolerance, time_limit):
        N = samples_to_keep
        self.face_distance = np.zeros([N,1])
        self.head_roll = np.zeros([N,1])
        self.head_pitch = np.zeros([N,1])
        self.head_yaw = np.zeros([N,1])
        self.face_height = np.zeros([N,1])
        self.last_notifiation_time = time.time()
    
    def set_references(self, face_distance_ref, face_height_ref, head_angle_ref):
        self.face_distance_ref = face_distance_ref
        self.face_height_ref = face_height_ref
        self.head_angle_ref = head_angle_ref

    def add_face_distance(self, new_face_distance):
        self.face_distances = self.rotate_and_add_to_array(self.face_distances, new_face_distance)
        self.find_face_distance_deviation()

    def find_face_distance_deviation(self):
        face_distance_dev = np.max(self.face_distances) - np.min(self.face_distances)
        if face_distance_dev > self.tol:
            self.notify("Pose Malone", "Think about your posture :)")

    '''
    Sends a OS X style notification to the user
    '''
    def notify(self, title, text):
        os.system("""
                osascript -e 'display notification "{}" with title "{}"'
                """.format(text, title))

    def rotate_and_add_to_array(self, array, new_element, shift = 1, axis = 0):
        array = np.roll(array, shift, axis)
        array[0] = new_element
        return array