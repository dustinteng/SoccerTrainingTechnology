import PoseEstimation as PE
import time
import cv2
import numpy as np 
pe = PE.PoseEstimation()

time_start = time.time()
first_iter = True
i=0
while (pe.cap_is_opened()):
    if first_iter == True:
        time_start = time.time()
        stopwatch = 0   
        first_iter = False
    else:
        stopwatch = round(time.time() - time_start, 2)

    success, data , processed_img = pe.loop_function(stopwatch) 
    # print(type(img))
    # print(processed_img)
    if success == True:
        # print(processed_img)
        cv2.imshow("Image", processed_img)
        cv2.waitKey(1)
    if 0xFF == ord('q'):
        break
# cv2.destroyAllWindows() 
    
