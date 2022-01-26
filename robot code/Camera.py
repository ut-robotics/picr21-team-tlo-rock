from asyncio import ALL_COMPLETED
import pyrealsense2 as rs
import cv2
import numpy as np
from enums import *
import math
import time
from functools import partial

def savefile(filename, values):
    save = open(filename, mode = 'w', encoding = 'UTF-8')
    for value in values:
        save.write(str(value) + '\n')
    save.close()
    print('Values saved to file', filename)

def checkBallLegitness(frame_yCoords):
    #for colour in reversed(frame_yCoords):
        #if colour[2] < 15:
            #print(colour)
            #return False
    return True

#Function for finding keypoints of one colour
def getKeyPoints(Trackbar_values, color_frame, FRAME_WIDTH, FRAME_HEIGHT, detector, MAX_KEYPOINT_COUNT, depth_image, color_image):
    # Colour detection limits

    lowerLimits = np.array(Trackbar_values[0:3])
    upperLimits = np.array(Trackbar_values[3:6])

    # Our operations on the frame come here
    thresholded_image = cv2.inRange(color_frame, lowerLimits, upperLimits)
    thresholded_image = cv2.bitwise_not(thresholded_image)
    thresholded_image = cv2.rectangle(thresholded_image, (0, 0), (FRAME_WIDTH-1, FRAME_HEIGHT-1), (255, 255, 255), 2)
    #detecting the blobs
    keypoints = detector.detect(thresholded_image)
    if MAX_KEYPOINT_COUNT > 1:
        tempKeypointX = np.zeros(MAX_KEYPOINT_COUNT, dtype=int)
        tempKeypointY = np.zeros(MAX_KEYPOINT_COUNT, dtype=int)
        tempKeypointZ = np.zeros(MAX_KEYPOINT_COUNT, dtype=int)
    else:
        tempKeypointX = [0]
        tempKeypointY = [0]
        tempKeypointZ = [0]

    i = 0 
    #printing the coordinates
    for punkt in keypoints:
        if i < MAX_KEYPOINT_COUNT:
            point_x = int(round(punkt.pt[0]))
            point_y = int(round(punkt.pt[1]))
            #print(punkt.pt)

            isLegit = True
            if MAX_KEYPOINT_COUNT != 1:
                frame_yColumn = []
                for j in range(point_y):
                    frame_yColumn.append(color_image[point_y][j])
                isLegit = checkBallLegitness(frame_yColumn)

            point_depth = int(depth_image.get_distance(point_x,point_y)*1000)
            #print(point_depth)
            if isLegit:
                tempKeypointX[i] = point_x
                tempKeypointY[i] = point_y
                tempKeypointZ[i] = point_depth
            i += 1

    output = [tempKeypointX.copy(), tempKeypointY.copy(), tempKeypointZ.copy()]
    return output

def fetchTrackbarValues(filename):
    try:
        defaults = open(filename, mode = 'r', encoding = 'UTF-8')
        trackbarValues = []
        for line in defaults:
            trackbarValues.append(int(line.strip()))
        defaults.close()
        return trackbarValues.copy()

    except:
        print("Failed loading", filename)

def setupCamera():
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    colorizer = rs.colorizer()
    colorizer.set_option(rs.option.visual_preset, 2)

    cam_res_width = 848
    cam_res_height = 480
    cam_fps = 60

    #camera product line is D400
    config.enable_stream(rs.stream.depth, cam_res_width, cam_res_height, rs.format.z16, cam_fps)
    config.enable_stream(rs.stream.color, cam_res_width, cam_res_height, rs.format.bgr8, cam_fps)

    # Start streaming
    pipeline_profile = pipeline.start(config)

    #configure exposure
    device = pipeline.get_active_profile().get_device().query_sensors()[1]
    device.set_option(rs.option.enable_auto_exposure,0)
    device.set_option(rs.option.enable_auto_white_balance,0)
    device.set_option(rs.option.exposure, 100.0)
    device.set_option(rs.option.white_balance, 50.0)
    
    #depth sensor parameters
    depth_sensor = pipeline_profile.get_device().first_depth_sensor()

    return (pipeline, cam_res_height, cam_res_width, colorizer)

def createblobdetector(minArea, maxArea):
    blobparams = cv2.SimpleBlobDetector_Params()

    blobparams.filterByArea = True
    blobparams.maxArea = maxArea
    blobparams.minArea = minArea
    blobparams.filterByInertia = False
    blobparams.filterByConvexity = False

    detector = cv2.SimpleBlobDetector_create(blobparams)
    return detector

def operate_camera(ballKeypointX, ballKeypointY, ballKeypointZ, attacking, BasketCoords):
    #________________________LOADING IN THE FILTERS__________________________________________
    colourLimitsGreen = fetchTrackbarValues('green.txt')
    colourLimitsPink = fetchTrackbarValues('pink.txt')
    colourLimitsBlue = fetchTrackbarValues('blue.txt')

    #___________________________________CAMERA SETUP_________________________________
    pipeline, cam_res_height, cam_res_width, colorizer = setupCamera()
    #________________________BLOB DETECTOR CREATION______________________________
    detector = createblobdetector(30, 700000)
    basketdetector = createblobdetector(200, 700000)

    #____________________ACTUAL OPERATIONS_____________________________________________________
    try:
        #cv2.namedWindow('cap', cv2.WINDOW_AUTOSIZE)
        #cv2.namedWindow('dist', cv2.WINDOW_AUTOSIZE)

        align_to = rs.stream.color
        align = rs.align(align_to)

        while True:
            if (attacking.value == Side.pink):
                colourLimitsBasket = colourLimitsPink
            else:
                colourLimitsBasket = colourLimitsBlue

            # Read the image from the camera
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            frames = align.process(frames)
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue
            
            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            #This will be sent to processing
            color_image = cv2.normalize(color_image, np.zeros((cam_res_width, cam_res_height)), 0, 255, cv2.NORM_MINMAX)
            color_image = cv2.rectangle(color_image, (280,0), (580,75), (0,0,255), -1)
            color_frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
            #outimage = color_frame.copy()
            

            #___________________FINDING KEYPOINTS________________________________________________
            MAX_KEYPOINT_COUNT = 11
            funcBallKeypointX, funcBallKeypointY, funcBallKeypointZ = getKeyPoints(colourLimitsGreen, color_frame, 
                                                        cam_res_width, cam_res_height, detector, 
                                                        MAX_KEYPOINT_COUNT, depth_frame, color_image)
            #print(funcBallKeypointX,funcBallKeypointY, funcBallKeypointZ)
            for i in range(MAX_KEYPOINT_COUNT):
                ballKeypointX[i] = funcBallKeypointX[i]
                ballKeypointY[i] = funcBallKeypointY[i]
                ballKeypointZ[i] = funcBallKeypointZ[i]

            basketx, baskety, basketz = getKeyPoints(colourLimitsBasket, color_frame, 
                                cam_res_width, cam_res_height, basketdetector, 
                                1, depth_frame, color_image)
            BasketCoords[0] = basketx[0]
            while (color_frame[baskety[0]][basketx[0]][2] < 165): #bgr
                baskety[0] -= 1
                if baskety[0] <= 0:
                    break
            BasketCoords[1] = baskety[0]
            BasketCoords[2] = basketz[0]
            #print(BasketCoords[0],BasketCoords[1],BasketCoords[2])

            #cv2.imshow('cap', outimage)
            #cv2.imshow('dist', depth_image)

            cv2.waitKey(1)
    
    except Exception as e:
        print(e)

    finally:
        # When everything done, release the capture
        print('closing camera')
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == '__main__':
 #__________________________HSV LEGACY____________________________________________
    try:
        defaults = open('trackbar_defaults.txt', mode = 'r', encoding = 'UTF-8')
        Trackbar_values = []
        for line in defaults:
            Trackbar_values.append(int(line.strip()))
        defaults.close()

    except:
        # Global variables for the trackbar value if no base file exists
        Trackbar_values = [29, 24, 69, 74, 171, 193, 5]

    # A callback function for a trackbar
    # It is triggered every time the trackbar slider is used
    def updateValue(value_index, new_value):
        Trackbar_values[value_index] = new_value
    
    trackbar_names = ['lH', 'lS', 'lV', 'hH', 'hS', 'hV', 'Mode(0-green, 1-black, 2-white, 3-pink, 4-blue)']
    trackbar_limits = [179, 255, 255, 179, 255, 255, 5]
    cv2.namedWindow("Trackbars")

    for index, name in enumerate(trackbar_names):
        cv2.createTrackbar(name, "Trackbars", Trackbar_values[index], trackbar_limits[index], partial(updateValue, index))
        
    #___________________________________CAMERA SETUP_________________________________
    pipeline, cam_res_height, cam_res_width, colorizer = setupCamera()

    #________________________BLOB DETECTOR CREATION___________________________________
    detector = createblobdetector(30, 700000)

    #____________________ACTUAL OPERATIONS_____________________________________________________
    try:
        align_to = rs.stream.color
        align = rs.align(align_to)

        while True:
            # Read the image from the camera
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            frames = align.process(frames)
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue
            
            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            #This will be sent to processing
            color_image = cv2.normalize(color_image, np.zeros((cam_res_width, cam_res_height)), 0, 255, cv2.NORM_MINMAX)
            color_image = cv2.rectangle(color_image, (280,0), (580,75), (0,0,255), -1)
            color_frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

            # Colour detection limits
            lowerLimits = np.array(Trackbar_values[0:3])
            upperLimits = np.array(Trackbar_values[3:6])

            # Our operations on the frame come here
            thresholded = cv2.inRange(color_frame, lowerLimits, upperLimits)
            thresholded = cv2.bitwise_not(thresholded)
            thresholded = cv2.rectangle(thresholded, (0, 0), (cam_res_width-2, cam_res_height-2), (255, 255, 255), 2)
            outimage = cv2.bitwise_and(color_frame, color_frame, mask = thresholded)

            #detecting the blobs
            keypoints = detector.detect(thresholded)
            img = cv2.drawKeypoints(color_image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            
            #printing the coordinates
            for punkt in keypoints:
                point_x = round(punkt.pt[0])
                point_y = round(punkt.pt[1])
                point_depth = int(depth_frame.get_distance(point_x,point_y)*1000)
                cv2.putText(outimage, str(point_x)+ ', ' + str(point_y) + ', ' + str(point_depth) , (point_x, point_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            #Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = np.asanyarray(colorizer.colorize(depth_frame).get_data())

            images = np.hstack((color_image, outimage))
            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)

            cv2.waitKey(1)

            #_____________________________CLEANUP AT THE END___________________________________________
            #save the threshold into a file
            if cv2.waitKey(1) & 0xFF == ord('s'):
                #Mode(0-green, 1-black, 2-white, 3-pink, 4-blue)
                savemap = ['green.txt', 'black.txt', 'white.txt', 'pink.txt', 'blue.txt', 'trackbar_defaults.txt']
                savefile(savemap[Trackbar_values[6]], Trackbar_values)

            # Quit the program when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    finally:
        savefile('trackbar_defaults.txt', Trackbar_values)

        # When everything done, release the capture
        print('closing program')
        pipeline.stop()
        cv2.destroyAllWindows()