import STTDevelopment as stt
import PoseEstimation as pe
import time
import cv2

stt = stt.STTDevelopment()
pe = pe.PoseEstimation()
shutdown = False
finish = False
stopwatch = 0
while not (shutdown):
    stt.user_login()
    stt.check_folder_number()
    
    while not (shutdown):
        menupick = stt.menu_pick()

        if menupick == '1':
            stt.begin_assessments()
            time_start = time.time()
            first_iter = True
            while (finish == False and shutdown == False):
                if first_iter == True:
                    time_start = time.time()
                    stopwatch = 0   
                    first_iter = False
                else:
                    stopwatch = round(time.time() - time_start, 2)

                success, data, img=  pe.loop_function(stopwatch)
                # print(success)
                if success == True:
                    cv2.imshow("live",img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        if menupick == '0':
            shutdown = True
            print('byebye')