import numpy as np
import cv2

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

def getKeyPoints(Trackbar_values, color_frame, FRAME_WIDTH, FRAME_HEIGHT, detector, MAX_KEYPOINT_COUNT, depth_image, depth_scale):
    # Colour detection limits
    lowerLimits = np.array(Trackbar_values[0:3])
    upperLimits = np.array(Trackbar_values[3:6])

    # Our operations on the frame come here
    thresholded_image = cv2.inRange(color_frame, lowerLimits, upperLimits)
    thresholded_image = cv2.bitwise_not(thresholded_image)
    thresholded_image = cv2.rectangle(thresholded_image, (0, 0), (FRAME_WIDTH-1, FRAME_HEIGHT-1), (255, 255, 255), 2)

    #detecting the blobs
    keypoints = detector.detect(thresholded_image)

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
            i += 1

    output = [tempKeypointX.copy(), tempKeypointY.copy(), tempKeypointZ.copy()]
    return output