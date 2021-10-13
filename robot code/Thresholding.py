import pyrealsense2 as rs
import cv2
import numpy as np
#__________________________DEPTH AVERAGING HELPER____________________________________________
def get_average_of_subarray(array, x, y, size):
    # get the rows and collumns to keep from the matrix
    lowcol = max(0, x-size)
    lowrow = max(0, y-size)
    
    highcol = min(array.shape[0], x+size+1)
    highrow = min(array.shape[1], y+size+1)

    # get the submatrix
    array = array[lowcol:highcol, lowrow:highrow]
    # if matrix has no values return 0
    if (array.size==0):
        return -1
    # return average/median of values in array
    return np.median(array)

if __name__ == '__main__':
    #__________________________HSV LEGACY____________________________________________
    try:
        defaults = open('trackbar_defaults.txt', mode = 'r', encoding = 'UTF-8')
        Trackbar_values = []
        for line in defaults:
            Trackbar_values.append(int(line.strip()))

        defaults.close()
        lH, lS, lV, hH, hS, hV = Trackbar_values

    except:
        # Global variables for the trackbar value if no base file exists
        lH = 29
        lS = 24
        lV = 69
        hH = 74
        hS = 151
        hV = 193

    # A callback function for a trackbar
    # It is triggered every time the trackbar slider is used
    def updateValueH(new_value):
        # Make sure to write the new value into the global variable
        global lH
        lH = new_value
    def updateValueS(new_value):
        # Make sure to write the new value into the global variable
        global lS
        lS = new_value
    def updateValueV(new_value):
        # Make sure to write the new value into the global variable
        global lV
        lV = new_value
    def updateValuehH(new_value):
        # Make sure to write the new value into the global variable
        global hH
        hH = new_value
    def updateValuehS(new_value):
        # Make sure to write the new value into the global variable
        global hS
        hS = new_value
    def updateValuehV(new_value):
        # Make sure to write the new value into the global variable
        global hV
        hV = new_value

    # Attach a trackbar to a window
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("H", "Trackbars", lH, 179, updateValueH)
    cv2.createTrackbar("S", "Trackbars", lS, 255, updateValueS)
    cv2.createTrackbar("V", "Trackbars", lV, 255, updateValueV)
    cv2.createTrackbar("hH", "Trackbars", hH, 179, updateValuehH)
    cv2.createTrackbar("hS", "Trackbars", hS, 255, updateValuehS)
    cv2.createTrackbar("hV", "Trackbars", hV, 255, updateValuehV)

    #___________________________________OPERATING CAMERA_________________________________
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    colorizer = rs.colorizer()
    colorizer.set_option(rs.option.visual_preset, 2)

    #camera product line is D400
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

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
    blobparams.maxArea = 700000
    blobparams.minArea = 30
    blobparams.filterByInertia = False
    blobparams.filterByConvexity = False

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
            color_image = cv2.normalize(color_image, np.zeros((640, 480)), 0, 255, cv2.NORM_MINMAX)
            color_frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

            height, width = (480, 640)

            #___________________HSV LEGACY________________________________________________
            # Colour detection limits
            lowerLimits = np.array([lH, lS, lV])
            upperLimits = np.array([hH, hS, hV])

            # Our operations on the frame come here
            thresholded = cv2.inRange(color_frame, lowerLimits, upperLimits)
            thresholded = cv2.bitwise_not(thresholded)
            thresholded = cv2.rectangle(thresholded, (0, 0), (width-1, height-1), (255, 255, 255), 2)
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

            # Quit the program when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:

        save = open('trackbar_defaults.txt', mode = 'w', encoding = 'UTF-8')
        Trackbar_values = [lH, lS, lV, hH, hS, hV]
        for value in Trackbar_values:
            save.write(str(value) + '\n')
        save.close()

        # When everything done, release the capture
        print('closing program')
        pipeline.stop()
        cv2.destroyAllWindows()
