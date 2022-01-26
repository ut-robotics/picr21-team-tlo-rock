#https://medium.com/vacatronics/3-ways-to-calibrate-your-camera-using-opencv-and-python-395528a51615

import pyrealsense2 as rs
import cv2
import numpy as np

def save_coefficients(mtx, dist, path):
    '''Save the camera matrix and the distortion coefficients to given path/file.'''
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
    cv_file.write('K', mtx)
    cv_file.write('D', dist)
    # note you *release* you don't close() a FileStorage object
    cv_file.release()

def load_coefficients(path):
    '''Loads camera matrix and distortion coefficients.'''
    # FILE_STORAGE_READ
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    camera_matrix = cv_file.getNode('K').mat()
    dist_matrix = cv_file.getNode('D').mat()

    cv_file.release()
    return [camera_matrix, dist_matrix]

def setupCamera():
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    colorizer = rs.colorizer()
    colorizer.set_option(rs.option.visual_preset, 2)

    cam_res_width = 640#848
    cam_res_height = 480
    cam_fps = 30

    #camera product line is D400
    config.enable_stream(rs.stream.depth, cam_res_width, cam_res_height, rs.format.z16, cam_fps)
    config.enable_stream(rs.stream.color, cam_res_width, cam_res_height, rs.format.bgr8, cam_fps)

    # Start streaming
    pipeline_profile = pipeline.start(config)

    #configure exposure
    device = pipeline.get_active_profile().get_device().query_sensors()[1]
    #device.set_option(rs.option.enable_auto_exposure,0)
    #device.set_option(rs.option.enable_auto_white_balance,0)
    #device.set_option(rs.option.exposure, 100.0)
    #device.set_option(rs.option.white_balance, 50.0)
    
    #depth sensor parameters
    depth_sensor = pipeline_profile.get_device().first_depth_sensor()

    return (pipeline, cam_res_height, cam_res_width, colorizer)

#__________________________________________________________________________________________________________________
chessboardWidth = 11
chessboardHeight = 8
square_size = 2.5 #cm
points = 0

# termination criteria
termcriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
objp = np.zeros((chessboardHeight*chessboardWidth, 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboardWidth, 0:chessboardHeight].T.reshape(-1, 2)

objp = objp * square_size

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
keypoints = []
keypoints2 = []

def calibrate_chessboard(image, width, height, criteria):
    '''Calibrate a camera using chessboard images.'''
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(image, (width, height), None)

    if ret:
        corners2 = cv2.cornerSubPix(image, corners, (11, 11), (-1, -1), criteria)
        return [corners, corners2]

#______________________________________________________________________________________________________________________

if __name__ == '__main__':
        
    #___________________________________CAMERA SETUP_________________________________
    pipeline, cam_res_height, cam_res_width, colorizer = setupCamera()

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
            #depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            #This will be sent to processing
            color_image = cv2.normalize(color_image, np.zeros((cam_res_width, cam_res_height)), 0, 255, cv2.NORM_MINMAX)
            #color_frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

            keypoints.clear()
            keypoints2.clear()
            output = calibrate_chessboard(color_image, chessboardWidth, chessboardHeight, termcriteria)
            if output != None:
                keypoints, keypoints2 = output
            print(output)

            images = color_image
            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)

            cv2.waitKey(1)

            #_____________________________ADMIN ACTIONS_______________________________________________________________
            #
            if cv2.waitKey(1) & 0xFF == ord('s'):
                objpoints.append(objp)
                imgpoints.append(keypoints2)
                print('Point number', points, 'data added!')
                points += 1

            # Quit the program when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    finally:
        if points >= 10:
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (cam_res_width, cam_res_height), None, None)
            save_coefficients(mtx, dist, "testing files/CalibrationMatrices.json")
            print('Camera calibration performed!')
            
        else:
            print('Not enough data to calibrate camera!')

        # When everything done, release the capture
        print('closing program')
        pipeline.stop()
        cv2.destroyAllWindows()