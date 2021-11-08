import serial
import struct
from time import sleep, time
from game_logic import stop
from serial.tools import list_ports


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

    max_speed_change =  100 #how much wheel speed can change in a second

    ser = None    #create serial connection
    prev_speeds = [0,0,0]
    #linear_velocity = overall_speed * math.cos(direction - math.radians(wheel_angle))

    #TODO use this: serial.tools.list_ports.comports instead of whats below
    ports = list_ports.comports()

    for port, desc, hwid in sorted(ports):
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

    #last_time = time()
    while run:
            sleep(0.001)
            #tme = time()
            #delta = min(tme - last_time, 1000 / max_speed_change) # delta cant be large enough to make the robots wheels overspin (failsafe)
            #print("delta", delta)
            #last_time = tme
            
            if running.value == 0:
                break

            if state.value == 0:
                send_motorspeeds(ser, *stop())
            
            if state.value in {1,2}:
                speeds = target_speeds[0:3]
                '''   
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
                '''

                ms = send_motorspeeds(ser, *(speeds + [target_speeds[3]]))

    if ser != None:
        ser.close()
    running.value = -1
    
