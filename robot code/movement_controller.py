from math import floor
import serial
import struct
from time import sleep, time
from game_logic import stop
from serial.tools import list_ports
from enums import *


COMMAND_STRUCT_FORMAT = '<hhhHBH'
FEEDBACK_STRUCT_FORMAT = '<hhhH'
FEEDBACK_STRUCT_SIZE = struct.calcsize(FEEDBACK_STRUCT_FORMAT)


#helpers
def send_motorspeeds(ser,m1 = 0,m2 = 0,m3 = 0,thrower = 0): # send speeds to motors and return data
    ser.write(struct.pack(COMMAND_STRUCT_FORMAT, m1, m2, m3, thrower, 0, 0xAAAA))
    data = ser.read(FEEDBACK_STRUCT_SIZE)
    values = struct.unpack(FEEDBACK_STRUCT_FORMAT, data)
    return values # returns motor data

def main(target_speeds, state, running):# main function of movement controller

    max_speed_change = 80 #how much wheel speed can change in a second

    ser = None    #create serial connection
    c_speeds = [0,0,0]
    i_speeds = [0,0,0]
    #linear_velocity = overall_speed * math.cos(direction - math.radians(wheel_angle))

    ports = list_ports.comports()

    for port, desc, _ in sorted(ports):
        print("{}: {}".format(port, desc))
        if desc == "STM32 Virtual ComPort":
            print("connecting...")
            try:
                ser = serial.Serial(port, baudrate=115200, timeout=3)
                print("connected")
                break
            except:
                print("connection attempt failed")    
            
    run = True
    changerate = 0

    last_time = time()
    while run:
            sleep(0.0001)
            tme = time()
            delta = tme - last_time
            #print("delta", delta)
            last_time = tme
            
            if running.value == 0:
                break

            if state.value == State.stopped._value_:
                send_motorspeeds(ser, *stop())
            
            if state.value in {State.automatic._value_,State.remote._value_}:
                n_speeds = target_speeds[0:3]
                #print(n_speeds, c_speeds)
                   
                mx = -1
                for i, v in enumerate(n_speeds):
                    if (tmp :=abs(v-c_speeds[i])) > mx:
                        mx = tmp
                if mx != 0:
                    
                    if mx > max_speed_change:
                        changerate = mx/(max_speed_change*min(delta,1))
                    else:
                        changerate = 1
                    for i, v in enumerate(c_speeds):
                        c_speeds[i] += (n_speeds[i]-v)/changerate  
                        i_speeds = [round(i) for i in c_speeds]
                             
                #print(c_speeds)

                ms = send_motorspeeds(ser, *(i_speeds + [target_speeds[3]]))
                #print(ms)

    if ser != None:
        ser.close()
    running.value = -1
    
