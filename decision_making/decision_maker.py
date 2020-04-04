import os
import time
import numpy as np

class Decision_maker:

    def __init__(self, samples_to_keep, distance_tolerance, head_angle_tolerance, face_height_tolerance, time_limit):
        N = samples_to_keep

        self.face_distance = np.zeros([N,1])
        self.face_distance_tol = distance_tolerance

        # roll, pitch, yaw
        self.head_angle = np.zeros([N,3])
        self.head_angle_tol = head_angle_tolerance

        self.face_height = np.zeros([N,1])
        self.face_height_tol = face_height_tolerance

        self.timestamps = np.zeros([N,1])

        self.start_of_bad_posture = None
        self.time_limit = time_limit

        self.last_notification_time = time.time()
    
    def set_references(self, face_distance_ref, head_angle_ref, face_height_ref):
        self.face_distance_ref = face_distance_ref
        self.face_height_ref = face_height_ref
        self.head_angle_ref = head_angle_ref

    def add_data(self, face_dist, head_angle, face_height):
        self.add_face_distance(face_dist)
        self.add_head_angle(head_angle)
        self.add_face_height(face_height)
        self.add_timestamp(time.time())
        return self.evalute_data()

    def add_face_distance(self, new_face_distance):
        self.face_distance = self.rotate_and_add_to_array(self.face_distance, new_face_distance)

    def add_head_angle(self, new_head_angle):
        self.head_angle = self.rotate_and_add_to_array(self.head_angle, new_head_angle)
    
    def add_face_height(self, new_face_height):
        self.face_height = self.rotate_and_add_to_array(self.face_height, new_face_height)

    def add_timestamp(self, timestamp):
        self.timestamps = self.rotate_and_add_to_array(self.timestamps, timestamp)

    def evalute_data(self):
        face_dist_ok = self.check_face_distance()
        face_height_ok = self.check_face_height()
        head_angle_ok = self.check_head_angle()

        if face_dist_ok and face_height_ok and head_angle_ok:
            self.start_of_bad_posture = None
            return True
        else:
            time_ok = self.check_time()
        if time_ok:
            return True
        else:
            return False


    def check_time(self):
        if self.start_of_bad_posture is None and (self.timestamps[0] - self.last_notification_time) > self.time_limit:
            self.start_of_bad_posture = self.timestamps[0]
            return True
        elif (self.timestamps[0] - self.start_of_bad_posture) < self.time_limit or (self.timestamps[0] - self.last_notification_time) < self.time_limit:
            return True
        else:
            self.start_of_bad_posture = None
            self.last_notification_time = time.time()
            return False


    def check_face_distance(self):
        if np.abs(self.face_distance[0] - self.face_distance_ref) > self.face_distance_tol:
            return False
        else:
            return True

    def check_face_height(self):
        if np.abs(self.face_height[0] - self.face_height_ref) > self.face_height_tol:
            return False
        else:
            return True

    def check_head_angle(self):
        relative_angle = self.head_angle[0]-self.head_angle_ref
        off_angle = np.sqrt(relative_angle[0]**2 + relative_angle[1]**2)
        if off_angle > self.head_angle_tol:
            return False
        else:
            return True

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

ds_maker = Decision_maker(10, 0.2, 19, 0.5, 30)
ds_maker.set_references(2, np.array([0, 0, 0]), 0)
no_notification_needed = ds_maker.add_data(0.2, np.array([0, 0, 0]), 0.1)
print(1+1)