import pyrealsense2 as rs
import cv2
import numpy as np
from functools import partial
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

def savefile(filename):
    global Trackbar_values
    save = open(filename, mode = 'w', encoding = 'UTF-8')
    for value in Trackbar_values:
        save.write(str(value) + '\n')
    save.close()
    print('Values saved to file', filename)

if __name__ == '__main__':
    #__________________________HSV LEGACY____________________________________________
    try:
        defaults = open('green.txt', mode = 'r', encoding = 'UTF-8')
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
        
    #___________________________________OPERATING CAMERA_________________________________
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
    depth_scale = depth_sensor.get_depth_scale()

    #________________________BLOB DETECTION PARAMETERS______________________________
    #detector object
    blobparams = cv2.SimpleBlobDetector_Params()

    blobparams.filterByArea = True
    blobparams.minArea = 30
    blobparams.maxArea = 70000000
    blobparams.filterByCircularity = False
    blobparams.filterByInertia = False
    
    detector = cv2.SimpleBlobDetector_create(blobparams)

    #____________________ACTUAL OPERATIONS_____________________________________________________
    try:
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
            color_frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

            #___________________HSV LEGACY________________________________________________
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
                point_depth = round(get_average_of_subarray(depth_image, point_x, point_y, 2)*depth_scale, 2)
                cv2.putText(outimage, str(point_x)+ ', ' + str(point_y) + ', ' + str(point_depth) , (point_x, point_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            #Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            #depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            depth_colormap = np.asanyarray(colorizer.colorize(depth_frame).get_data())

            images = np.hstack((color_image, outimage))
            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)

            #_____________________________CLEANUP AT THE END___________________________________________
            cv2.waitKey(1)

            #save the threshold into a file
            if cv2.waitKey(1) & 0xFF == ord('s'):
                #Mode(0-green, 1-black, 2-white, 3-pink, 4-blue)
                savemap = ['green.txt', 'black.txt', 'white.txt', 'pink.txt', 'blue.txt', 'trackbar_defaults.txt']
                savefile(savemap[Trackbar_values[6]])

            # Quit the program when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    finally:
        savefile('trackbar_defaults.txt')

        # When everything done, release the capture
        print('closing program')
        pipeline.stop()
        cv2.destroyAllWindows()
