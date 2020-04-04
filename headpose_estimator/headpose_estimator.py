import os
import cv2
import sys
import numpy as np
from math import cos, sin
import numpy as np
from keras.layers import Average
# Add the path of the external library from top folder
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'headpose_estimator/external/FSA-Net')))
from lib.FSANET_model import *


class HeadPoseEstimator:
    def __init__(self):
        self.model = self.init_model()

    def init_model(self):
        self.imsize = 64
        stage_num = [3,3,3]
        #Parameters
        num_capsule = 3
        dim_capsule = 16
        routings = 2
        stage_num = [3,3,3]
        lambda_d = 1
        num_classes = 3
        num_primcaps = 7*3
        m_dim = 5

        S_set = [num_capsule, dim_capsule, routings, num_primcaps, m_dim]
        model1 = FSA_net_Capsule(self.imsize , num_classes, stage_num, lambda_d, S_set)()
        model2 = FSA_net_Var_Capsule(self.imsize , num_classes, stage_num, lambda_d, S_set)()
        
        num_primcaps = 8*8*3
        S_set = [num_capsule, dim_capsule, routings, num_primcaps, m_dim]

        model3 = FSA_net_noS_Capsule(self.imsize , num_classes, stage_num, lambda_d, S_set)()

        print('Loading models ...')
        model_file_location = 'headpose_estimator/external/FSA-Net'
        weight_file1 = model_file_location + '/pre-trained/300W_LP_models/fsanet_capsule_3_16_2_21_5/fsanet_capsule_3_16_2_21_5.h5'
        model1.load_weights(weight_file1)
        print('Finished loading model 1.')
        
        weight_file2 = model_file_location + '/pre-trained/300W_LP_models/fsanet_var_capsule_3_16_2_21_5/fsanet_var_capsule_3_16_2_21_5.h5'
        model2.load_weights(weight_file2)
        print('Finished loading model 2.')

        weight_file3 = model_file_location + '/pre-trained/300W_LP_models/fsanet_noS_capsule_3_16_2_192_5/fsanet_noS_capsule_3_16_2_192_5.h5'
        model3.load_weights(weight_file3)
        print('Finished loading model 3.')
        print('Finished loading models ...')


        inputs = Input(shape=(self.imsize ,self.imsize ,3))
        x1 = model1(inputs) #1x1
        x2 = model2(inputs) #var
        x3 = model3(inputs) #w/o
        avg_model = Average()([x1,x2,x3])
        return Model(inputs=inputs, outputs=avg_model)

    def estimate_headpose(self, face_img, render = False):
        face = face_img.copy()
        faces = np.empty((1, self.imsize, self.imsize, 3))
        
        faces[0,:,:,:] = cv2.resize(face, (self.imsize, self.imsize))
        faces[0,:,:,:] = cv2.normalize(faces[0,:,:,:], None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)        
        
        face = np.expand_dims(faces[0,:,:,:], axis=0)
        p_result = self.model.predict(face)
        face = face.squeeze()
        img = None

        if render:
            img = draw_axis(face_img, p_result[0][0], p_result[0][1], p_result[0][2])

        return p_result, img




def draw_axis(img, yaw, pitch, roll, tdx=None, tdy=None, size = 50):
    pitch = pitch * np.pi / 180
    yaw = -(yaw * np.pi / 180)
    roll = roll * np.pi / 180

    if tdx != None and tdy != None:
        tdx = tdx
        tdy = tdy
    else:
        height, width = img.shape[:2]
        tdx = width / 2
        tdy = height / 2

    # X-Axis pointing to right. drawn in red
    x1 = size * (cos(yaw) * cos(roll)) + tdx
    y1 = size * (cos(pitch) * sin(roll) + cos(roll) * sin(pitch) * sin(yaw)) + tdy

    # Y-Axis | drawn in green
    #        v
    x2 = size * (-cos(yaw) * sin(roll)) + tdx
    y2 = size * (cos(pitch) * cos(roll) - sin(pitch) * sin(yaw) * sin(roll)) + tdy

    # Z-Axis (out of the screen) drawn in blue
    x3 = size * (sin(yaw)) + tdx
    y3 = size * (-cos(yaw) * sin(pitch)) + tdy

    cv2.line(img, (int(tdx), int(tdy)), (int(x1),int(y1)),(0,0,255),3)
    cv2.line(img, (int(tdx), int(tdy)), (int(x2),int(y2)),(0,255,0),3)
    cv2.line(img, (int(tdx), int(tdy)), (int(x3),int(y3)),(255,0,0),2)

    return img