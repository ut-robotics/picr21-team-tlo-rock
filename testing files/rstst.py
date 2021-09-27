#camera code
#https://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/opencv_viewer_example.py
import pyrealsense2 as rs
import numpy as np
import cv2

#thresholding crap


blobparams = cv2.SimpleBlobDetector_Params()
blobparams.filterByInertia = False
blobparams.filterByConvexity = False
blobparams.filterByArea = True
blobparams.filterByCircularity = False
blobparams.minArea = 100
blobparams.maxArea = 100000
blobparams.filterByColor = True
blobparams.blobColor = 255
blobparams.minDistBetweenBlobs = 10
detector = cv2.SimpleBlobDetector_create(blobparams)

global lB
global lG
global lR
global hB
global hG
global hR

min_x_dist = 5

drivetime = 3

try:
    f = open('trackbar_defaults.txt','r')
    data = f.read().splitlines()
    f.close()
    data2 = []
    for i in data:
        data2.append(int(i))
    lB, lG, lR, hB, hG, hR = data2
except:
    lB = 0
    lG = 70
    lR = 156
    hB = 48
    hG = 255
    hR = 255

max_y_dist = 2



global kernel_size
kernel_size = 5

global closing
closing = 3

def update_closing_size(new_value):
    global closing
    closing = new_value


def update_kernel_size(new_value):
    global kernel_size
    kernel_size = new_value*2+1

def lBf(new_value):
    # Make sure to write the new value into the global variable
    global lB
    lB = new_value

def lGf(new_value):
    # Make sure to write the new value into the global variable
    global lG
    lG = new_value

def lRf(new_value):
    # Make sure to write the new value into the global variable
    global lR
    lR = new_value

def hBf(new_value):
    # Make sure to write the new value into the global variable
    global hB
    hB = new_value

def hGf(new_value):
    # Make sure to write the new value into the global variable
    global hG
    hG = new_value

def hRf(new_value):
    # Make sure to write the new value into the global variable
    global hR
    hR = new_value





kernel = np.ones((5,5),np.uint8)
cv2.namedWindow("thresholded")
cv2.namedWindow("Original")

cv2.createTrackbar("lB", "thresholded", lB, 255, lBf)
cv2.createTrackbar("lG", "thresholded", lG, 255, lGf)
cv2.createTrackbar("lR", "thresholded", lR, 255, lRf)
cv2.createTrackbar("hB", "thresholded", hB, 255, hBf)
cv2.createTrackbar("hG", "thresholded", hG, 255, hGf)
cv2.createTrackbar("hR", "thresholded", hR, 255, hRf)
cv2.createTrackbar("update_kernel_size", "Original", int((kernel_size-1)/2), 10, update_kernel_size)
cv2.createTrackbar("update_closing_size", "Original", closing, 10, update_closing_size)
                                                                           



# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))
colorizer = rs.colorizer()
colorizer.set_option(rs.option.visual_preset, 2)

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        #print(depth_frame.get_distance(320,240))
        #print('---------------')

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        #depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        depth_colormap = np.asanyarray(colorizer.colorize(depth_frame).get_data())
        


        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            frame = cv2.blur(resized_color_image,(kernel_size,kernel_size))
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))
            frame = cv2.blur(color_image,(kernel_size,kernel_size))

        
        #frame = cv2.medianBlur(frame,kernel_size)
        #frame = cv2.bilateralFilter(frame,9,75,75)
        #frame = cv2.GaussianBlur(frame,(kernel_size,kernel_size),0)
        

        
        lowerLimits = np.array([lB, lG, lR])
        upperLimits = np.array([hB, hG, hR])
        
        

        # Our operations on the frame come here
        thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
        thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel, iterations = closing)
        outimage = cv2.bitwise_and(frame, frame, mask = thresholded)
        thresholded = cv2.rectangle(thresholded, (0, 0), (frame.shape[1]-1, frame.shape[0]-1), (0, 0, 0), 2)
        
        keypoints = detector.detect(thresholded)
        #print (keypoints)
        frame = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        for i in range(len(keypoints)):
                x_cord = int(keypoints[i].pt[0])
                y_cord = int(keypoints[i].pt[1])
                cv2.putText(frame, f"({x_cord}, {y_cord})", (x_cord, y_cord), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Original', frame)

        # Display the resulting frame
        #cv2.imshow('Processed', outimage)
        cv2.imshow('thresholded', thresholded)
            
        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        if cv2.waitKey(1) == ord('q'):
            break

finally:

    # Stop streaming
    pipeline.stop()