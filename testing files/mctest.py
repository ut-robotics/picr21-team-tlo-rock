from time import sleep
max_speed_change = 2
delta = 0.28
c_speeds = [0,0,0]
n_speeds = [0,-4,3]

while True:
    mx = -1
    for i, v in enumerate(n_speeds):
        if (tmp :=abs(v-c_speeds[i])) > mx:
            mx = tmp
    if mx != 0:
        print(mx)
        if mx > max_speed_change:
            changerate = mx/(max_speed_change*min(delta,1))
        else:
            changerate = 1
        print(changerate)
        for i, v in enumerate(c_speeds):
            print((n_speeds[i]-v)/changerate)
            c_speeds[i] += (n_speeds[i]-v)/changerate
    print(c_speeds)
    sleep(1)