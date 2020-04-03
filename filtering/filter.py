import numpy as np

class filter:

    def __init__(self, fps, seconds_to_keep):
        # Frames per second for application
        self.fps = fps
        # Data-elements in use
        N = fps * seconds_to_keep
        # Raw face_distance at all time instances
        self.face_distance = np.empty([N, 1])
        # Raw bounding boxes used as [x, y, width, height]
        self.bounding_boxes = np.empty([N, 4])
        # Areas for corresponding bounding boxes
        self.bounding_box_areas = np.empty([N, 1])

    def add_bounding_box(self, new_bounding_box):
        self.bounding_boxes = self.rotate_and_add_to_array(self.bounding_boxes, new_bounding_box)
        self.update_areas()

    def update_areas(self):
        # Area is width * height
        area = self.bounding_boxes[0][2] * self.bounding_boxes[0][3]
        self.bounding_box_areas = self.rotate_and_add_to_array(self.bounding_box_areas, area)

    def rotate_and_add_to_array(self, array, new_element, shift = 1, axis = 0):
        array = np.roll(array, 1, 0)
        array[0] = new_element
        return array


    def get_face_distance(self):
        pass



Filter = filter(5, 3)
for i in range(0,20):
    Filter.add_bounding_box(np.array([i, i + 1,  i + 2, i + 3]))

print(1+1)