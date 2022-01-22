
import time
def find_nearest_ball(keypointsX, keypointsY, keypointsZ):
    #print("------")
    temp_ball = [0, 0, 0]
    closest_index = 0

    for i in range(11):
        #print(keypointsX[i],keypointsY[i], keypointsZ[i])
        #print(keypointsX[i], keypointsZ[i]) 
        if (keypointsZ[i] <= keypointsZ[closest_index]) and (keypointsZ[i] != 0):
            closest_index = i
            temp_ball[0] = keypointsX[closest_index]
            temp_ball[1] = keypointsY[closest_index]
            temp_ball[2] = keypointsZ[closest_index]
    if temp_ball[0] == 0 and temp_ball[1] == 0:
        return None
    
    return temp_ball

def localize(BALLkeypointsX, BALLkeypointsY, BALLkeypointsZ, nearest_ball, time_of_no_ball):
    last_time = time.time()
    while True:
        current_time = time.time()
        delta = current_time-last_time
        last_time = current_time
        function_output = find_nearest_ball(BALLkeypointsX, BALLkeypointsY, BALLkeypointsZ)
        #print(function_output)
        if function_output != None:
            nearest_ball[0] = function_output[0]
            nearest_ball[1] = function_output[1]
            nearest_ball[2] = function_output[2]
            time_of_no_ball.value = 0
        else:
            time_of_no_ball.value += delta