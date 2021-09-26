''' This file is 3/3 of 
    the Soccer Training Technology's developed at UCSD for 
    1. MAE 199 - Spring 2021 with prof Jack Silberman and prof Mauricio de Oliveira
    2. Triton AI - STT 

    pose_estimation.py
    check user's body pose estimation (17 points in 2D)

    camera: Logitec HD Pro Webcam C920 (mtx and dist are calibrated)
    device: X86 NVIDIA GTX 2070 Super running on linux

    This file deals with 
    1. running the model 
    2. creating pose estimation real time
    3. saving data to a JSON file

    creator: Jan Dustin Tengdyantono
    maintainer: Jan, Jonathan
'''

import os
from argparse import ArgumentParser
from config_dir import config
import cv2
from mmpose.apis import (inference_bottom_up_pose_model, init_pose_model,vis_pose_result)

class PoseEstimation(object):
    def __init__(self):
        self._pose_config = config.POSE_CONFIG
        self._pose_checkpoint = config.POSE_CHECKPOINT
        self._device = config.POSE_DEVICE
        self._video_path = config.CAM_PATH
        self._nms_thr = config.POSE_NMS_THR
        self._kpt_thr = config.POSE_KPT_THR
        self._return_heatmap = config.POSE_RETURN_HEATMAP
        self._output_layer_names = config.POSE_OUTPUT_LAYER_NAMES
        self._show = config.POSE_SHOW
        
        # turning video on
        self._cap = cv2.VideoCapture(self._video_path)

        # build the pose model from a config file and a checkpoint file
        self._pose_model = init_pose_model(
                self._pose_config, self._pose_checkpoint , self._device )
        self._dataset = self._pose_model.cfg.data['test']['type']
        self._bool_cam = False #check if camera feed is available
        self._bool_data = False #check if pose estimation is being done properly
        self._img = None
        self._data = []
        self._vis_img = None


        assert (self._dataset == 'BottomUpCocoDataset')

    def cap_is_opened(self):
        """check if camera is currently active 
    
            param None
            return: bool
        """
        return self._cap.isOpened()

    def loop_function(self, stopwatch):
        """ Pose Estimation loop function that checks each frame's feed
            
            runs pose estimation and store the data into a variable that will be used in stt_main.py

            returns:    bool_cam (if camera is providing feed), 
                        bool_data, 
                        self._data, 
                        self._img
        """

        #  valiable initialization
        l_ankle = None
        r_ankle = None
        self._bool_cam = False
        self._bool_data = False
        self._data = []
        self._img = None # current camera feed
        self._vis_img = None # to be checked and drawn


        # check if camera feed is available
        self._bool_cam, self._img = self._cap.read()   
        if self._bool_cam == True:
            # perform pose estimation
            pose_results, returned_outputs = inference_bottom_up_pose_model(
                self._pose_model,
                self._img,
                self._nms_thr,
                self._return_heatmap,
                outputs = self._output_layer_names)
            # print('poseRes', pose_results)

            # show the results on the current frame
            self._vis_img = vis_pose_result(
                self._pose_model,
                self._img,
                pose_results,
                dataset=self._dataset,
                kpt_score_thr=self._kpt_thr,
                show=False)
            # cv2.imshow("Image", self._img)
            # if self._show:
            #     cv2.imshow('frames', self._vis_img)
            
            # print(pose_results) - the length of the list is the number of people 
            if len(pose_results) > 0:
                if len(pose_results[0]) > 0 and len(pose_results[0]['keypoints']) > 0:
                    l_ankle = pose_results[0]['keypoints'][15]
                    r_ankle = pose_results[0]['keypoints'][16]
                    # print("left ankle: ", str(l_ankle))
                    # print("right ankle: ", str(r_ankle))
    
                l_ankle_x = l_ankle[0]
                l_ankle_y = l_ankle[1]
                l_ankle_s = l_ankle[2] # score
                r_ankle_x = r_ankle[0]
                r_ankle_y = r_ankle[1]
                r_ankle_s = r_ankle[2] # score

                # check if data is correct (the location in pixel is greater than 0)
                if l_ankle_x >=0 and l_ankle_y >= 0:
                    if r_ankle_x >=0 and r_ankle_y >= 0:
                        success = True

                        center_x = (abs(l_ankle_x) + abs(r_ankle_x))/2
                        center_y = (abs(l_ankle_y) + abs(r_ankle_y))/2
                        center_s = round(l_ankle_s * r_ankle_s,2)
                        self._data ={
                                        "time": stopwatch,
                                        "left_ankle": {
                                            "x" : l_ankle_x,
                                            "y" : l_ankle_y,
                                            "score": l_ankle_s
                                        },
                                        "right_ankle": {
                                            "x" : r_ankle_x,
                                            "y" : r_ankle_y,
                                            "score": r_ankle_s
                                        },
                                        "center": {
                                            "x" : center_x,
                                            "y" : center_y,
                                            "score": center_s 
                                        }
                                    }
                        
                    return self._bool_cam, self._data, self._vis_img

                else:
                    self._data = None
                    self._img = None
                    return self._bool_cam, self._data, self._vis_img
        

            else:
                return self._bool_cam, self._data, self._vis_img
        else:
            return self._bool_cam, self._data, self._vis_img
