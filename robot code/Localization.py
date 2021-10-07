def find_nearest_ball(keypointsX, keypointsZ):
    nearest_ball = [0, 0]
    i = 0
    for i in range(11):
        if keypointsZ[i] <= nearest_ball[1] and keypointsZ != 0:
            nearest_ball[0] = keypointsX[i]
            nearest_ball[1] = keypointsZ[i]

    print(nearest_ball)
    return nearest_ball



def localize(BALLkeypointsX, BALLkeypointsZ, nearest_ball):
    while True:
        function_output = find_nearest_ball(BALLkeypointsX, BALLkeypointsZ)
        nearest_ball[0] = function_output[0]
        nearest_ball[1] = function_output[1]