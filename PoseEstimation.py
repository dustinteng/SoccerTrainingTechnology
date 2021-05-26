import os
from argparse import ArgumentParser

import cv2

from mmpose.apis import (inference_bottom_up_pose_model, init_pose_model,
                         vis_pose_result)


# no need to use parser

class PoseEstimation(object):
    
    def __init__(self):
        self._pose_config = 'hrnet_w32_coco_512x512.py'
        self._pose_checkpoint = 'https://download.openmmlab.com/mmpose/bottom_up/hrnet_w32_coco_512x512-bcb8c247_20200816.pth' 
        self._device = 'cuda:0'
        self._video_out = ''
        self._video_path = '/dev/video0'
        self._nms_thr = 0.9 #OKS threshold for pose NMS - non maximum suppression
        self._kpt_thr = 0.3 # key point score threshold
        self._return_heatmap = False
        self._output_layer_names = None
        self._show = True
        self._img = None
        self._vis_img = None
        # turning video on
        self._cap = cv2.VideoCapture(self._video_path)

        # build the pose model from a config file and a checkpoint file
        self._pose_model = init_pose_model(
                self._pose_config, self._pose_checkpoint , self._device )
        self._dataset = self._pose_model.cfg.data['test']['type']


        assert (self._dataset == 'BottomUpCocoDataset')

    def cap_is_opened(self):
        return self._cap.isOpened()

    def loop_function(self, stopwatch):
        ret, img = self._cap.read()

        if ret == True:
            pose_results, returned_outputs = inference_bottom_up_pose_model(
                self._pose_model,
                img,
                self._nms_thr,
                self._return_heatmap,
                outputs = self._output_layer_names)
            # print('poseRes', pose_results)
            l_ankle = None
            r_ankle = None
            data = None

            if len(pose_results) > 0:
                if len(pose_results[0]) > 0 and len(pose_results[0]['keypoints']) > 0:
                    l_ankle = pose_results[0]['keypoints'][15]
                    r_ankle = pose_results[0]['keypoints'][16]
                    # print("left ankle: ", str(l_ankle))
                    # print("right ankle: ", str(r_ankle))
                else:
                    data = None
                    img = None
                    success = False

                    return success, data, img
    
    
                # show the results
                self._vis_img = vis_pose_result(
                    self._pose_model,
                    img,
                    pose_results,
                    dataset=self._dataset,
                    kpt_score_thr=self._kpt_thr,
                    show=False)
                # cv2.imshow("Image", img)

            
                # if self._show:
                #     cv2.imshow('frames', self._vis_img)
                    
                l_ankle_x = l_ankle[0]
                l_ankle_y = l_ankle[1]
                l_ankle_s = l_ankle[2]
                r_ankle_x = r_ankle[0]
                r_ankle_y = r_ankle[1]
                r_ankle_s = r_ankle[2]
        
                center_x = (abs(l_ankle_x) + abs(r_ankle_x))/2
                center_y = (abs(l_ankle_y) + abs(r_ankle_y))/2
                center_s = round(l_ankle_s * r_ankle_s,2)
                data = (
                                {
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
                                    
                                }}
                        )
            success = True
            return success, data, self._vis_img

        else:
            data = None
            img = None
            success = False

            return success, data, img
