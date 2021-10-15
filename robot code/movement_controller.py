from cv2 import integral
import serial
import struct
import math
from time import sleep, time

#helpers
def send_ms(ser,speeds): #unpacks motorspeeds
    return send_motorspeeds(ser,speeds[0],speeds[1],speeds[2],speeds[3]) #returns motor data

def send_motorspeeds(ser,m1 = 0,m2 = 0,m3 = 0,thrower = 0): # send speeds to motors and return data
    ser.write(struct.pack('<hhhHBH', m1, m2, m3, thrower, 0, 0xAAAA))
    size = struct.calcsize('<hhhH')
    data = ser.read(size)
    values = struct.unpack('<hhhH',data)
    return values #returns motor data

def stop():
    return [0, 0, 0, 0]

def main(target_speeds, state, running):# main function of movement controller

    max_speed_change =  10 #how much wheel speed can change in a second


    ser = None    #create serial connection
    prev_speeds = [0,0,0]
    #linear_velocity = overall_speed * math.cos(direction - math.radians(wheel_angle))

    last_time = time()

    try:
        port='/dev/ttyACM0'
        ser = serial.Serial(port, baudrate=115200, timeout=3)

        run = True

        while run:
            tme = time()
            delta = tme - last_time # delta
            
            if running.value == 0:
                break

            if state.value == 0:
                send_ms(ser, stop())
            

            if state.value == 1:
                #print(target_speeds[0])
                #target_speeds = [100,100,100, 0]
                speeds = target_speeds[0:3]
                
                mx = 0 # suurim kiiruste erinevus
                for i, v in enumerate(speeds):
                    speeds[i] = v-prev_speeds[i]
                    if abs(v-prev_speeds[i]) > mx:
                        mx = abs(i)
                
                #mx - maximum change
                if mx == 0:
                    changerate = 0
                else:
                    changerate = max_speed_change * delta / mx

                prev_speeds = [int(v+speeds[i]*changerate) for i,v in enumerate(prev_speeds)]

                print(prev_speeds)
                

                send_ms(ser, prev_speeds + [target_speeds[3]])
            sleep(0.001)


    except Exception as e:
        print(e)
    if ser != None:
        ser.close()
    running.value = -1
    
