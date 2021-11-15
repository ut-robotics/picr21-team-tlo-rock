import pyrealsense2 as rs
import cv2
import numpy as np

#__________________________DEPTH AVERAGING HELPER____________________________________________
def get_average_of_subarray(array, x, y, size):
    #848 x 480
    # get the rows and collumns to keep from the matrix
    lowrow = max(0, x-size)
    lowcol = max(0, y-size)
    
    highrow = min(array.shape[0], x+size+1)
    highcol = min(array.shape[1], y+size+1)

    # get the submatrix
    array = array[lowrow:highrow, lowcol:highcol]
    #print(array)
    
    # if matrix has no values return -1
    if (array.size==0):
        return -1
    #return average/median of values in array
    #return np.median(array)
    return np.max(array)

def operate_camera(keypointX, keypointZ):
    #__________________________HSV LEGACY____________________________________________
    try:
        defaults = open('green.txt', mode = 'r', encoding = 'UTF-8')
        Trackbar_values_green = []
        for line in defaults:
            Trackbar_values_green.append(int(line.strip()))
        defaults.close()

    except:
        # Global variables for the trackbar value if no base file exists
        Trackbar_values_green = [22, 16, 56, 98, 173, 158, 0]

    #___________________________________CAMERA SETUP_________________________________
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    #colorizer = rs.colorizer()
    #colorizer.set_option(rs.option.visual_preset, 2)

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
    depth_scale = depth_sensor.get_depth_scale()*1000

    #________________________BLOB DETECTION PARAMETERS______________________________
    #detector object
    blobparams = cv2.SimpleBlobDetector_Params()

    blobparams.filterByArea = True
    blobparams.maxArea = 700000
    blobparams.minArea = 30
    blobparams.filterByInertia = False
    blobparams.filterByConvexity = False

    detector = cv2.SimpleBlobDetector_create(blobparams)

    #____________________ACTUAL OPERATIONS_____________________________________________________
    try:
        cv2.namedWindow('cap', cv2.WINDOW_AUTOSIZE)
        #cv2.namedWindow('dist', cv2.WINDOW_AUTOSIZE)
        while True:
            # Read the image from the camera
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue
            
            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            #This will be sent to processing
            color_image = cv2.normalize(color_image, np.zeros((cam_res_width, cam_res_height)), 0, 255, cv2.NORM_MINMAX)
            color_image = cv2.rectangle(color_image, (380,0), (480,30), (192,150,4), -1)
            color_frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

            #___________________HSV LEGACY________________________________________________
            # Colour detection limits
            lowerLimits_green = np.array(Trackbar_values_green[0:3])
            upperLimits_green = np.array(Trackbar_values_green[3:6])

            # Our operations on the frame come here
            thresholded_green = cv2.inRange(color_frame, lowerLimits_green, upperLimits_green)
            thresholded_green = cv2.bitwise_not(thresholded_green)
            thresholded_green = cv2.rectangle(thresholded_green, (0, 0), (cam_res_width-1, cam_res_height-1), (255, 255, 255), 2)
            outimage = cv2.bitwise_and(color_frame, color_frame, mask = thresholded_green)

            #detecting the blobs
            keypoints = detector.detect(thresholded_green)
           
            MAX_KEYPOINT_COUNT = 11
            tempKeypointX = np.zeros(MAX_KEYPOINT_COUNT, dtype=int)
            tempKeypointY = np.zeros(MAX_KEYPOINT_COUNT, dtype=int)
            tempKeypointZ = np.zeros(MAX_KEYPOINT_COUNT, dtype=int)
            
            i = 0 
            #printing the coordinates
            for punkt in keypoints:
                if i < MAX_KEYPOINT_COUNT:
                    point_x = int(round(punkt.pt[0]))
                    point_y = int(round(punkt.pt[1]))
                    point_depth = int(round(get_average_of_subarray(depth_image, point_y, -point_x, 2)*depth_scale, 2))
                    tempKeypointX[i] = point_x
                    tempKeypointY[i] = point_y
                    tempKeypointZ[i] = point_depth
                    cv2.putText(outimage, str(point_x)+ ', ' + str(point_y) + ', ' + str(point_depth) , (point_x, point_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    i += 1
            
            #print(tempKeypointX)
            #print("-----")
            for i in range(MAX_KEYPOINT_COUNT):
                keypointX[i] = tempKeypointX[i]
                keypointZ[i] = tempKeypointZ[i]
                #print(keypointX[i], keypointZ[i])
            
            cv2.imshow('cap', outimage)
            #cv2.imshow('dist', depth_image)
            cv2.waitKey(1)
    
    except Exception as e:
        print(e)

    finally:
        # When everything done, release the capture
        print('closing camera')
        pipeline.stop()