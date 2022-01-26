from math import floor
import serial
import struct
from time import sleep, time
from serial.tools import list_ports

COMMAND_STRUCT_FORMAT = '<hhhHIL'
FEEDBACK_STRUCT_FORMAT = '<hhhBL'

FEEDBACK_STRUCT_SIZE = struct.calcsize(FEEDBACK_STRUCT_FORMAT)
print(struct.calcsize(COMMAND_STRUCT_FORMAT))
def send_motorspeeds2(ser,m1 = 0,m2 = 0,m3 = 0,thrower = 4000, grabber = True, throw = True): # send speeds to motors and return data
    bools = int(grabber*2+throw)
    ser.write(struct.pack(COMMAND_STRUCT_FORMAT, int(m1), int(m2), int(m3), bools, int(thrower), 0xAAAA))
    data = ser.read(FEEDBACK_STRUCT_SIZE)
    ser.reset_input_buffer()
    values = struct.unpack(FEEDBACK_STRUCT_FORMAT, data)
    print(values)
    return(values) # returns motor data

def send_motorspeeds(ser,m1 = 0,m2 = 0,m3 = 0,thrower = 0): # send speeds to motors and return data
    ser.write(struct.pack(COMMAND_STRUCT_FORMAT, int(m1), int(m2), int(m3), int(thrower), 0xAAAA))
    data = ser.read(FEEDBACK_STRUCT_SIZE)
    print(data)
    values = struct.unpack(FEEDBACK_STRUCT_FORMAT, data)
    return( values )# returns motor data




ports = list_ports.comports()
ser = None    #create serial connection

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


print(ser)
c = 1
f = open("väärtused.txt", "w")
this = 0
last = 0
while (c > 0):
    
    f.write(str((this := send_motorspeeds2(ser)[1])-last) +","+ str(time())+"\n")
    last = this
    c-=1
f.close()
print("done")

