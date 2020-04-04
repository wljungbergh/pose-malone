import numpy as np
'''
Filter class
Keeps track of data for given number of samples. Outputs mean of data over samples. 
'''
class Filter:

    def __init__(self, samples_to_keep, shape = [1]):
        # Data-samples to use
        N = samples_to_keep
        # Raw data
        self.data = np.empty([N, *shape])

    def add_data(self, new_data):
        # Add new bounding box from external
        self.data = self.rotate_and_add_to_array(self.data, new_data)
        self.smoothen()

    def smoothen(self):
        self.smooth_data = np.mean(self.data, axis=0)

    def get_smooth_data(self):
        return self.smooth_data

    def rotate_and_add_to_array(self, array, new_element, shift = 1, axis = 0):
        array = np.roll(array, shift, axis)
        array[0] = new_element
        return array