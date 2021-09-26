''' This file is 2/3 of 
    the Soccer Training Technology's developed at UCSD for 
    1. MAE 199 - Spring 2021 with prof Jack Silberman and prof Mauricio de Oliveira
    2. Triton AI - STT 

    aruco_checker.py
    check area play boundary by detecting 4 ArUco markers on the floor to be recognized as the boundary
    camera: Logitec HD Pro Webcam C920 (mtx and dist are calibrated)
    device: X86 NVIDIA GTX 2070 Super running on linux

    This file deals with 
    1. area bound reading
    2. averaging plane transformation matrix
    3. saving matrix transformation data to a JSON file

    creator: Jan Dustin Tengdyantono
    maintainer: Jan, Jonathan
'''

import cv2
import numpy as np
import time
import os
import json
from config_dir import config

# constants
a_width, a_height = config.AREA_WIDTH, config.AREA_HEIGHT  #2D warped 


class ArucoChecker(object):
    def __init__(self):
        # camera properties
        self._cam_path = config.CAM_PATH
        self._mtx = config.CAM_MATRIX
        self._dist = config.CAM_DISTORTION
        self._fps = config.CAM_FPS
        # ArUco and calibration properties
        self._side_length = config.ARUCO_SIZE
        self._cal_dict = config.ARUCO_DICTIONARY
        self._cal_frames = []
        self._cal_time = config.ARUCO_TIMER
        # warping properties
        self._trf_mtx = None

    # helper function
    def camera_check(self):
        """ 
            Display real time camera feed to help with the calibration
        """
        # Create an object to read from camera
        video = cv2.VideoCapture(self._cam_path)
        # We need to check if camera is opened previously or not
        if (video.isOpened() == False): 
            print(config.S_ERR_VIDEO)
            
        print(config.S_CAMERA_POS_CHECK)
        while(video.isOpened):
            ret, frame = video.read()
            if ret == True:
    
                cv2.imshow('Calibration Frames', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    # helper function #1: 
    def detecting_markers_location(self, image):
        """ Detecting all Aruco Markers Locations and depicting each markers capability per frame

            Using CV2, the ArUco markers are used as reference for the area bound (assessment area)
            this helper function is used by the area_calibraion_run function

            :param <np array> image: image (per frame)
            :returns:  boolean, tvecs, ids, marked_image
        """
        # print(type(image))
        # image = Image.fromarray(np.array(image))
        
        markers, ids, rejected = cv2.aruco.detectMarkers(image, dictionary = self._cal_dict, cameraMatrix = self._mtx, distCoeff = self._dist)
        if not np.any(markers):
            return False, [], [], []
        
        rvecs, tvecs, objPoints = cv2.aruco.estimatePoseSingleMarkers(markers, self._side_length, self._mtx, self._dist)

        if not np.any(tvecs):
            return False, [], [], []

        assert (len(markers) == len(ids) == len(tvecs)), "Must have same number of markers, ids and tvecs"

        image_copy = np.copy(image)
        cv2.aruco.drawDetectedMarkers(image_copy, markers)
        for i in range(len(ids)):
            cv2.aruco.drawAxis(image_copy, self._mtx, self._dist, rvecs[i], tvecs[i], 0.05)
            marker = markers[i][0]
            x, y, z = marker[0][0], marker[0][1], tvecs[i][0][2]
            x = int(x)
            y = int(y)
            image_area_marked = cv2.putText(img=image_copy, text="id = {0:d}".format(ids[i][0]), org=(x,y), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(0, 0, 255), thickness=2)

        return ids, markers, image_area_marked 

    # helper function #2: 
    def warp_markers(self, image, images_count, ids, markers):
        """ checking detected markers and warp it 
            
            when all aruco markers are obtained inside a frame, the data will then be appended.
            this helper function is used by the area_calibraion_run function

            param [np array] image : current image
            param int images_count : non-faulty images count
            returns float array : location of each inner verteces - markers are not included to the frame
        """

        X = False
        try:
            mark1 = np.where(ids == [1])[0][0]
            mark2 = np.where(ids == [2])[0][0]
            mark3 = np.where(ids == [3])[0][0]
            mark4 = np.where(ids == [4])[0][0]

            # X is True when all aruco markers are detected properly
            X = True
        except IndexError:
            print("one or more markers are not detected")

        if X == True:
            one = np.float32(markers[mark1][0][2])
            two = np.float32(markers[mark2][0][3])
            three = np.float32(markers[mark3][0][1])
            four = np.float32(markers[mark4][0][0])

            data = [one,two,three,four,images_count]
            return X, data
        else:
            data = [0,0,0,0,0]
            return X, data

    # functions: calibration run that calls helper function #1 and #2
    def area_calibration_run(self, frames):
        """ calibration run that calls function detecting_markers_location and warp_markers

            checking play area boundary by averaging the location of the markers
            uses both detecting_markers_location and warp_markers functions

            args: frames

            returns: transformation matrix
        """

        N = len(frames)
        one = []
        two = []
        three = []
        four = []

        images_count = 0
        cal_frame_trgt = config.ARUCO_CALIBRATION_FRAME_TARGET
        # checking detected markers and averaging the locations
        for n in range(N):
            if images_count < cal_frame_trgt:
                image = frames[n]
                
                #detecting area bound
                ids, markers, image_area_marked = self.detecting_markers_location(image) #1
                success, data = self.warp_markers(image, images_count, ids, markers) #2
                if success == True:
                    one.append(data[0])
                    two.append(data[1])
                    three.append(data[2])
                    four.append(data[3])
                    images_count = data[4] + 1 #checking image count for average geometric translation matrix
        print(str(images_count) + ' stable images')

        # error checking if the camera can detect all bourdaries {target} times
        if images_count == cal_frame_trgt :
        
            # averaging the location of each markers
            loc_one = np.float32(sum(one)/len(one))
            loc_two = np.float32(sum(two)/len(two))
            loc_three = np.float32(sum(three)/len(three))
            loc_four = np.float32(sum(four)/len(four))

            # perspective transformation
            point2 = np.float32([[0,0],[a_width,0],[0,a_height],[a_width,a_height]])
            point1 = np.float32([loc_one,loc_two,loc_three,loc_four])
            matrix = cv2.getPerspectiveTransform(point1,point2)
            image_warped = cv2.warpPerspective(image,matrix,(a_width,a_height))
            
            # show ArUco markers area boundary
            print(' Transformation Matrix:', matrix)
            
            #showing area from #helper1
            image = image_area_marked
            cv2.imshow("Area Calibration", image)
            # showing warped images 
            cv2.imshow("Warped", image_warped)
            success = True 
            time.sleep(2)
            cv2.destroyAllWindows()
            return matrix, success
        
        if images_count < cal_frame_trgt :
            print(config.S_NOT_SUCCESS_CAL_ARUCO)
            success = False
            matrix = None
            return matrix, success


    # functions: record video 
    def record_calibration_video(self):
        """ recording camera frames append it to a list type variable
        
        appending frames to cal_frame variable - heap memory allocation
        did this in order to boost efficiency

        appending list type variable self._cal_frames

        return: None
        
        """
        
        video = cv2.VideoCapture(self._cam_path)
        # We need to check if camera is opened previously or not
        if (video.isOpened() == False): 
            print("Error reading video file")

        # create start time and frame counter
        time_start = time.time()
        time_now = time_start
        while(video.isOpened):
            ret, frame = video.read()
            time_now= time.time()
            if ret == True:
                # result.write(frame)
                self._cal_frames.append(frame)
                delta_t = time_now - time_start
                # break after 
                if delta_t > self._cal_time and cv2.waitKey(1):
                    break 
            # Break the loop
            else:
                break
        # When everything done, release the video capture and video write objects
        video.release()
        # Closes all the frames
        # cv2.destroyAllWindows()	


    def calibrate_JSON(self):
        """ creating a JSON ArUco calibration file :

            adding calibration data to be saved later on

            return : saving calibration data as JSON file
        """
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        # trf_mtx = self._trf_mtx.tolist()
        data = (
            {
                "time": current_time,
                # "camera_matrix": self._trf_mtx
            }
        )
        return data

    def ArUco_main(self):
        """ This Function executes boundary area calibration

            checking area bound by detecting 4 ArUco markers on the floor

            return: Transformation Matrix
        """
            
        
        self.record_calibration_video()

        ######################################
        run = self.area_calibration_run(self._cal_frames)
        trf_mtx, success = run
        # print('check point')
        if success:
            self._trf_mtx = trf_mtx
            print(trf_mtx)
            return self._trf_mtx
            
        if not success:
            print(config.S_ADJUST_CAMERA)
            self.camera_check()
            self.ArUco_main()
        