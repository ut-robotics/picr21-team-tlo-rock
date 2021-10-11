def find_nearest_ball(keypointsX, keypointsZ):
    '''
    for i in range(11):
        print('keypoint ', i)
        print(keypointsX[i])
        print(keypointsZ[i])
    print("-------------")
    '''
    
    temp_ball = [0, 0]

    closest_index = 0
    for i in range(11):
        if (keypointsZ[i] <= keypointsZ[closest_index]) and (keypointsZ[i] != 0):
            #print(keypointsZ[i])
            closest_index = i
            temp_ball[0] = keypointsX[closest_index]
            temp_ball[1] = keypointsZ[closest_index]

    return temp_ball

def localize(BALLkeypointsX, BALLkeypointsZ, nearest_ball):
    while True:
        function_output = find_nearest_ball(BALLkeypointsX, BALLkeypointsZ)
        nearest_ball[0] = function_output[0]
        nearest_ball[1] = function_output[1]