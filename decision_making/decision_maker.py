import os
import time
import numpy as np

class DecisionMaker:

    def __init__(self, samples_to_keep, distance_tolerance, head_angle_tolerance, face_height_tolerance, time_limit):
        '''
        Input:
            samples_to_keep -- integer, specifying the number of samples to save
            distance_tolerance -- double, tolerance for how much face may move closer to/further from camera from initial position
            head_angle_tolerance -- double, how much the head may tilt away from original position before considered bad
            face_height_tolerance -- double, how much the face may move down in the image before considered batch_dot
            time_limit -- int, how many seconds a continously bad posture must be kept before notifying user
        '''
        N = samples_to_keep

        self.face_distance = np.zeros([N,1])
        self.face_distance_tol = distance_tolerance

        # roll, pitch, yaw
        self.head_angle = np.zeros([N,1])
        self.head_angle_tol = head_angle_tolerance

        self.face_height = np.zeros([N,1])
        self.face_height_tol = face_height_tolerance

        self.timestamps = np.zeros([N,1])

        self.start_of_bad_posture = None
        self.time_limit = time_limit

        self.last_notification_time = time.time()
    
    def set_references(self, face_distance_ref, head_angle_ref, face_height_ref):
        '''
        Set reference values for face distance, head angle and face height.
        Must be called before adding data. 
        Input:
            face_distance_ref - double
            face_height_ref - np.array([row, pitch, yaw])
            head_angle_ref - double
        '''
        self.face_distance_ref = face_distance_ref
        self.face_height_ref = face_height_ref
        self.head_angle_ref = head_angle_ref

    def add_data(self, face_dist, head_angle, face_height):
        '''
        Call method to add newly collected data to decision maker. Automatically adds timestamps for when method is called.
        When new data is added, data is evaluated if posture is bad and for how long.

        Input:
            face_dist: double - current value for face distance from screen
            head_angle: numpy array for current values of [roll, pitch, yaw]
            face_height: double - current value for face height

        Output:
            boolean: False if user should be notified about posture. True otherwise.
        '''
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
        print("1: {}".format(self.start_of_bad_posture))
        print("2: {}".format(self.time_limit))
        print("3: {}".format(self.last_notification_time))

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

    def notify(self, title, text):
        '''
        Sends a OS X style notification to the user
        '''
        os.system("""
                osascript -e 'display notification "{}" with title "{}"'
                """.format(text, title))

    def rotate_and_add_to_array(self, array, new_element, shift = 1, axis = 0):
        array = np.roll(array, shift, axis)
        array[0] = new_element
        return array