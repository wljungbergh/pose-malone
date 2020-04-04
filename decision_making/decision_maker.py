import os
import time
import numpy as np

class Decision_maker:

    def __init__(self, samples_to_keep, distance_tolerance, head_angle_tolerance, face_height_tolerance, time_limit):
        N = samples_to_keep

        self.face_distance = np.zeros([N,1])
        self.face_distance_time = np.zeros([N,1])
        self.face_distance_tol = distance_tolerance

        self.head_angles = np.zeros([N,3])
        self.head_angles_time = np.zeros([N,1])
        self.head_angles_tol = head_angle_tolerance

        self.face_height = np.zeros([N,1])
        self.face_height_time = np.zeros([N,1])
        self.face_height_tol = face_height_tolerance

        self.last_notifiation_time = time.time()
    
    def set_references(self, face_distance_ref, face_height_ref, head_angle_ref):
        self.face_distance_ref = face_distance_ref
        self.face_height_ref = face_height_ref
        self.head_angle_ref = head_angle_ref

    def add_data(self, face_dist, head_angle, face_height):
        timestamp = time.time()
        self.add_face_distance(face_dist, timestamp)
        self.add_head_angles(head_angle, timestamp)
        self.add_face_height(face_height, timestamp)
        return self.evalute_data()

    def add_face_distance(self, new_face_distance, timestamp):
        self.face_distances = self.rotate_and_add_to_array(self.face_distances, new_face_distance)
        self.face_distances_time = self.rotate_and_add_to_array(self.face_distances_time, timestamp)

    def add_head_angles(self, new_head_angle, timestamp):
        self.head_angles = self.rotate_and_add_to_array(self.head_angles, new_head_angle)
        self.head_angles_time = self.rotate_and_add_to_array(self.head_angles_time, timestamp)
    
    def add_face_height(self, new_face_height, timestamp):
        self.face_height = self.rotate_and_add_to_array(self.face_height, new_face_height)
        self.face_height_time = self.rotate_and_add_to_array(self.face_height_time, timestamp)

    def evalute_data(self):
        face_dist_ok = self.check_face_distance()
        face_height_ok = self.check_face_height()
        head_angle_ok = self.check_head_angle()
        if face_dist_ok and face_height_ok and head_angle_ok:
            return True
        else:
            return False

    def check_face_distance(self):
        if np.abs(self.face_distance[0] - self.face_distance_ref) > self.face_distance_tol:
            return False
        else:
            return True

    def check_face_height(self):
        pass

    def check_head_angle(self):
        pass

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