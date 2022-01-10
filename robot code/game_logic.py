import math
from time import sleep, time
from enums import *

#helpers

#combine 2 movement vectors together with some ratio (default 1 to 1)
def combine_moves(move1, move2, p1 = 1, p2 = 1):
    speed = [0,0,0,0]
    for i,v in enumerate(move1):
        speed[i]+= v*p1
    for i,v in enumerate(move2):
        speed[i]+= v*p2
    return speed#returns new movement vector (motor speeds)

def stop():
    return [0, 0, 0, 0]

def linear_velocity(speed, angle, wheel_angle):
    return int(speed * math.cos(math.radians(angle) - math.radians(wheel_angle)))

def move_omni(speed, angle): #generate movement vector with direction and speed
    
    WHEEL_ANGLES = [210, 330, 90]
    #linear_velocity = overall_speed * math.cos(direction - math.radians(wheel_angle))
    return [linear_velocity(speed, angle, wheel_angle) for wheel_angle in WHEEL_ANGLES] + [0]
    #return list(map(linear_velocity,[[speed,angle,210],[speed,angle,330],[speed,angle,90]])) + [0]

def rotate_omni(speed, mults = [1,1,1]): # generate rotation vector with speed
    speed = int(speed)
    return[speed * mult for mult in mults] + [0]

def thrower(speed): # generate rotation vector with speed
    return[0,0,0,speed]

def minimax(v, minim, maxim):
    return max(min(v, maxim),minim)

def rectify_speed(object, max_speed): #changes the biggest wheel speed to be the same as given speed but keeps all ratios the same
    obj = object[0:len(object)-1]
    mx = 0
    for i in obj:
        ai = abs(i)
        if ai > mx:
            mx = ai
    if mx == 0:
        return[0,0,0,0]
    if mx < max_speed:
        return object
    mx = max_speed/mx
    object = [int(element * mx) for element in object]
    return object # returns the correctedmovement vector

def set_speed(target_speeds,speed):
    for i in range(len(speed)):
        target_speeds[i] = speed [i]

def searching(gs, noball, speeds):
    #print(noball.value)
    if noball.value == 0:
        print("moveto")
        return GameState.moveto
    set_speed(speeds, rotate_omni(8))
    return gs

def moveto(gs, noball, nearest_ball, speeds):
    if noball.value > 0.1:
        gs = GameState.searching
        print("moveto to searching")
        return gs

    #print(nearest_ball[0], nearest_ball[1])
    error = (nearest_ball[0]-424)/4.24
      
    if nearest_ball[1] < 280:
        gs = GameState.orbit
        print("orbit")
    else:
        #print(int(math.floor(error ** 1.05 * 0.1)))
        movement_vector = rotate_omni(int(math.floor(error * 0.04)))
        movement_vector = combine_moves(movement_vector, move_omni(25,0))
        speed = 50
        if nearest_ball[1] < 1000:
            speed = 30
        movement_vector = rectify_speed(movement_vector,speed)
        set_speed(speeds, movement_vector)
    return gs

def pid(x, kp, ki, kd, piddat):
    piddat[0]+=x
    integral = piddat[0]
    derivative = piddat[1]-x
    piddat[1] = x
    return(x * kp + integral * ki + derivative * kd)

def orbit_a(gs, nearest_ball, noball, basket, speeds, pids):
    if nearest_ball[1] > 350 or noball.value > 0.1:
        return GameState.moveto
    
    spd = 20
    
    dif = (basket[0] - nearest_ball[0])/848
    hdelta = nearest_ball[0]/424-1
    vdelta = (math.sin(((nearest_ball[1])*math.pi)/960)) - 0.6

    if (abs(dif)< 0.01 and abs(hdelta)< 0.15 and abs(vdelta)< 0.1):
        return GameState.launch

    movment_vector = move_omni(int(pid(vdelta, 1, 0, 1, pids[0])*spd), 0)
    print(dif,hdelta,  vdelta,basket[0], nearest_ball[0])
    movment_vector = combine_moves(move_omni(int(pid(dif, 4, 0, 0, pids[1])*spd),90),movment_vector)
    movment_vector = combine_moves(rotate_omni(pid(hdelta, 0.4, 0, 0.1, pids[2])*spd, [1,1,0]),movment_vector)
    movment_vector = rectify_speed(movment_vector, 20)
    set_speed(speeds,movment_vector)
    return gs



    



def orbit(gs, nearest_ball, noball, basket, speeds): #old orbiter code
    #print("o", nearest_ball[0],nearest_ball[1],nearest_ball[2])
    if nearest_ball[1] > 300 or noball.value > 0.1:
        gs = GameState.moveto
        return gs
    
    tgt = [basket[0], basket[1], basket[2]]
    #print("basket",basket[0],basket[1],basket[2])
    #if noball.value > 0.5:
    #    gs = GameState.searching
    #print(nearest_ball[0],nearest_ball[1])
    # distance from robot tgt 130
    # side to side tgt 424,425

    spd = 20
    if abs(tgt[0] - 424) < 60:
        spd = 3
    elif abs(tgt[0] - 424) < 424:
        spd = 5
    

    movement_vector = move_omni(minimax((nearest_ball[1]-160)*0.18,-spd,spd),0)
    movement_vector = combine_moves(movement_vector, rotate_omni(minimax((nearest_ball[0]-424)*0.04, -spd,spd), [1,1,0]))
    movement_vector = combine_moves(movement_vector, rotate_omni(minimax((nearest_ball[0]-424), 3,-3), [1,1,0]))
    #movement_vector = combine_moves(movement_vector, move_omni(max(min((nearest_ball[0]-424)*0.1, 3),-3),90))
    print(movement_vector)
    if abs(tgt[0] - 424) <= 5 and abs(nearest_ball[0]-424) <= 5:
        gs = GameState.launch
    elif tgt[0] > 424:
        movement_vector = combine_moves(movement_vector, move_omni(spd, 90))
        combine_moves(movement_vector, rotate_omni(-5))
    elif tgt[0] < 424:
        movement_vector = combine_moves(movement_vector, move_omni(-spd, 90))
        combine_moves(movement_vector, rotate_omni(5))
    
    #movement_vector = rectify_speed(movement_vector, 20)
    #print(movement_vector)
    set_speed(speeds,movement_vector)
    return gs

def launch(gs, launchdelay, speeds, delta, tgt, nearest_ball, launch_time):
    if launchdelay[0] < 1:
        set_speed(speeds,stop())
        launchdelay[0] += delta
        #print(tgt)
    else:
        movement_vector = move_omni(5,0)
        #print(int(0.05*(tgt[1]-350)**2+560)) # 0.05\left(x-350\right)^{2}\ +560
        #movement_vector = combine_moves(movement_vector, thrower(int(0.05*(tgt[1]-350)**2+570)))
        #movement_vector = combine_moves(movement_vector, thrower(int(0.000006*(tgt[1]-340)**4+560)))
        #movement_vector = combine_moves(movement_vector, thrower(int(0.00038*(tgt[1]-344)**3+610)))
        #4.7x-1800
        movement_vector = combine_moves(movement_vector, thrower(int(4.7*tgt[2]-1800))) #https://www.desmos.com/calculator/gumsqpcewh
        print(tgt[0],tgt[1],tgt[2])
        set_speed(speeds,movement_vector)
        launch_time[0] += delta
        
        if launch_time[0] > 6:
            launchdelay[0] = 0
            launch_time[0] = 0
            gs = GameState.searching
    return gs

def main(nearest_ball, speeds, state, noball, basket):# main function of movement controller 
    sleep(0.5)
    #while True:
    #    set_speed(speeds, thrower(550)) 
    #    print(speeds[0],speeds[1],speeds[2],speeds[3])
    
    # pid constants
    #Kp = 0.8
    #Ki = 0.9
    #Kd = 0.6

    launchdelay = [0]

    gs = GameState.orbit

    tgt = [0,0,0]

    launch_time = [0]
    pids = [[0,0],[0,0],[0,0]]

    last_time = time()
    while True:
        current_time = time()
        delta = current_time-last_time
        last_time = current_time

        #orbit_a(gs, nearest_ball, noball, basket, speeds)

        if (state.value != State.automatic):
            continue
        #print(nearest_ball[0], nearest_ball[1],nearest_ball[2])
        if  gs == GameState.searching:
            gs = searching(gs, noball, speeds)
        elif gs == GameState.moveto:
            gs = moveto(gs, noball, nearest_ball, speeds)
        elif gs == GameState.orbit:
            gs = orbit(gs, nearest_ball, noball, basket, speeds)
            #gs = orbit_a(gs, nearest_ball, noball, basket, speeds, pids)
        elif gs == GameState.launch:
            gs = launch(gs, launchdelay, speeds, delta, basket, nearest_ball, launch_time)
        else:
            gs = GameState.searching
            print("reset")




# 379 - 600
# 407 - 700
# 418 - 800
