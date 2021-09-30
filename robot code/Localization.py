def find_nearest_ball(keypointsX, keypointsZ):
    nearest_ball = [0, 0]
    i = 0
    for i in range(11):
        if keypointsZ <= nearest_ball[1] and keypointsZ != 0:
            nearest_ball[0] = keypointsX[i]
            nearest_ball[1] = keypointsZ[i]
    return nearest_ball



def localize(BALLkeypointsX, BALLkeypointsZ):
    while True:
        target = find_nearest_ball(BALLkeypointsX, BALLkeypointsZ)