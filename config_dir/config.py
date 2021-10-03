from pathlib import Path
import numpy as np
import cv2

"""
HEIGHT = 180
WEIGHT = 100
UPLOAD_DIR = '~/ksdcjnkjcdsnoui'
CAMERA_CALIBRATION = [[0,0,1],[1,0,0]]

FIVE_POINTS_DIR = Path("~/test-result/five_points").expanduser()
FIVE_POINT_NAME = FIVE_POINTS_DIR.parent.name # five_points
"""

#camera properties:
CAM_PATH = Path('/dev/video0')
CAM_MATRIX = np.mat([[1.35007461e+03, 0.00000000e+00, 9.64381787e+02],[0.00000000e+00, 1.34859409e+03, 6.10803328e+02],[0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
CAM_DISTORTION = np.mat([ 0.10485946, -0.24625137, 0.00903166, -0.00257263, -0.09894589])
CAM_FPS = 30

#area play / freeroam constants:
AREA_WIDTH: 360
AREA_HEIGHT: 360

#aruco and calibration properties
ARUCO_DICTIONARY = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
ARUCO_SIZE = 19 # in cm
ARUCO_TIMER = 6 #n seconds * 30fps (timer for calibration)
ARUCO_CALIBRATION_FRAME_TARGET = 10 #only need to take 10 stable images (all arucos noticed)

#pose estimation properties:
POSE_CONFIG = 'hrnet_w32_coco_512x512.py'
POSE_CHECKPOINT = 'https://download.openmmlab.com/mmpose/bottom_up/hrnet_w32_coco_512x512-bcb8c247_20200816.pth' 
POSE_DEVICE = 'cuda:0'
POSE_NMS_THR = 0.9 #OKS threshold for pose NMS - non maximum suppression
POSE_KPT_THR = 0.3 #key point score threshold
POSE_OUTPUT_LAYER_NAMES = None #keep it this way if you don't know what you're doing
POSE_RETURN_HEATMAP = False #keep it this way if you don't know what you're doing
POSE_SHOW = True #keep it this way if you don't know what you're doing

#stt_main.py properties
MAIN_DISPLAY = 'display://0'
MAIN_STOPWATCH = 0


#strings
S_CAMERA_POS_CHECK = "if camera is in position, press q to continue"
S_NOT_SUCCESS_CAL_ARUCO = "not successfully calibrating assessment area"
S_ERR_VIDEO = "Error reading video, please check the hardware connection or the CAM_PATH constant"
S_ADJUST_CAMERA = " Camera can't see every aruco markers clearly, please adjust the camera"


