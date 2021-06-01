import PoseEstimation as PE
import STTDevelopment as STT
import time
import cv2
import numpy as np 
pe = PE.PoseEstimation()
stt = STT.STTDevelopment()

time_start = time.time()
first_iter = True

bool_cam = False
bool_data = False
data = []
processed_img = None

i=0
while (pe.cap_is_opened()):
    bool_cam = False
    bool_data = False

    if first_iter == True:
        time_start = time.time()
        stopwatch = 0   
        first_iter = False
    else:
        stopwatch = round(time.time() - time_start, 2)

    bool_cam, bool_data , data, processed_img = pe.loop_function(stopwatch) 
    # print(type(img))
    if bool_cam == True:
        # print(processed_img)
        cv2.imshow("Image", processed_img)
        cv2.waitKey(5)
    if bool_cam == True and bool_data == True:
        loc_3d_x = data['center']['x']
        loc_3d_y = data['center']['y']
        print('x  : ', loc_3d_x)
        print('y  : ', loc_3d_y)

    else:
        print('false data')
    if 0xFF == ord('q'):
        break

# cv2.destroyAllWindows() 
    
