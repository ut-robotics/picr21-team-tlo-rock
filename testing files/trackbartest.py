import cv2
import numpy as np

lH = 0

# A callback function for a trackbar
# It is triggered every time the trackbar slider is used
def updateValue(new_value, trackbar_variable):
    # Make sure to write the new value into the global variable
    trackbar_variable = new_value

# Attach a trackbar to a window
cv2.namedWindow("Trackbars")
cv2.createTrackbar("H", "Trackbars", lH, 179, updateValue, userdata=lH)

while True:
    print(lH)