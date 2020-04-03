import numpy as np
'''
Filter class
Keeps track of given number of bounding boxes and their area. Outputs face distance. 
'''
class Filter:

    def __init__(self, samples_to_keep):
        # Data-samples to use
        N = samples_to_keep
        # Raw face_distance at all time instances
        self.face_distance = 0
        # Raw bounding boxes used as [x, y, width, height]
        self.bounding_boxes = np.empty([N, 4])
        # Areas for corresponding bounding boxes
        self.bounding_box_areas = np.empty([N, 1])

    def add_bounding_box(self, new_bounding_box):
        # Add new bounding box from external
        self.bounding_boxes = self.rotate_and_add_to_array(self.bounding_boxes, new_bounding_box)
        # Update areas to match bounding_boxes
        self.update_areas()

    def update_areas(self):
        # Area is width * height
        area = self.bounding_boxes[0][2] * self.bounding_boxes[0][3]
        self.bounding_box_areas = self.rotate_and_add_to_array(self.bounding_box_areas, area)
        # Calculate new smooth face_distance based on current bounding_box_areas
        self.update_face_distance()

    def update_face_distance(self):
        self.face_distance = np.mean(self.bounding_box_areas)

    def get_face_distance(self):
        return self.face_distance

    def rotate_and_add_to_array(self, array, new_element, shift = 1, axis = 0):
        array = np.roll(array, 1, 0)
        array[0] = new_element
        return array
