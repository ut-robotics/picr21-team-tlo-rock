def find_nearest_ball(keypointsX, keypointsZ):
    nearest_ball = [0, 0]
    i = 0
    for i in range(11):
        if keypointsZ[i] <= nearest_ball[1] and keypointsZ != 0:
            nearest_ball[0] = keypointsX[i]
            nearest_ball[1] = keypointsZ[i]
    return nearest_ball

def localize(BALLkeypointsX, BALLkeypointsZ, nearest_ball):
    while True:
        nearest_ball = find_nearest_ball(BALLkeypointsX, BALLkeypointsZ)