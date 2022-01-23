import cv2

image = 'testing files/bluearucopng.png'

arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
arucoParams = cv2.aruco.DetectorParameters_create()
(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,
	parameters=arucoParams)