#!/usr/bin/env python

import pyrealsense2 as rs
import cv2

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
#device = pipeline.get_active_profile().get_device().query_sensors()[1]
#device.set_option(rs.option.exposure, 320.0)
#device.set_option(rs.option.enable_auto_exposure,0)
#device.set_option(rs.option.enable_auto_white-balance,0)

#depth sensor parameters
depth_sensor = pipeline_profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

#________________________BLOB DETECTION PARAMETERS______________________________
#detector object
blobparams = cv2.SimpleBlobDetector_Params()

blobparams.filterByArea = True
blobparams.maxArea = 700000
blobparams.minArea = 200
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
        cv2.imshow(color_frame, "tst")
        cv2.waitKey(1)
finally:
    # When everything done, release the capture
    print('closing camera')
    pipeline.stop()