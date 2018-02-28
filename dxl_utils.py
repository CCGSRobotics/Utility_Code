"""
This code requires first installing the pyax12 Python package.
- http://pyax-12.readthedocs.io/en/latest/index.html

Pyax12 is a Python 3 package which can be installed on a Linux/OSX machine like so:

sudo pip3 install pyax12

Servos must already have an ID set before the below functions can be used.
You'll need to use something like Dynamixel Manager to set the ID on each
servo - https://github.com/Interbotix/dynaManager/releases

# OTHER METHODS TO PLAY WITH
#def read_data(self, dynamixel_id, address, length)
#def write_data(self, dynamixel_id, address, data)
#def ping(self, dynamixel_id)
# Sync_Write = 0x83

PACKET STRUCTURE
    +----+----+--+------+-----+----------+---+-----------+---------+
    |0XFF|0XFF|ID|LENGTH|ERROR|PARAMETER1|...|PARAMETER N|CHECK SUM|
    +----+----+--+------+-----+----------+---+-----------+---------+

"""

import time
from pyax12.connection import Connection
from pyax12.packet import *
from emuBot import *

sc = Connection(port="/dev/usb2ax", baudrate=1000000)

# For connecting to USB2AX on OSX
#sc = Connection(port="/dev/tty.usbmodem1461", baudrate="1000000")


# Print useful information about an individual dynamixel servo
def dxlInfo(ID):                
        sc.flush()
        sc.pretty_print_control_table(ID)

def getAvailableDxl():
        sc.flush()
        lst = sc.scan()
        new_list = []
        for dxl in lst:
              new_list.append("ID " + str(dxl))

        return new_list

def reset(ID):
        AX_HEADER = 0xFF
        PK_LENGTH = 0x02
        AX_WRITE = 0x06
        AX_PARAM1 = 0x00
        AX_PARAM2 = 0x00
        CHECKSUM = compute_checksum(bytes((ID, PK_LENGTH, AX_WRITE))) 

        sc.flush()
        sc.send(bytes((AX_HEADER, AX_HEADER, ID, PK_LENGTH, AX_WRITE, CHECKSUM)))
        print("instruction packet sent... wait 5 seconds")
        time.sleep(5)
        print("Dynamixel has been reset and ID is set to '1'")
        
def reboot(ID):
        AX_HEADER = 0xFF
        ID = 0xFD
        PK_LENGTH = 0x05
        ERROR = 0x01
        AX_WRITE = 0x03
        AX_PARAM1 = 0x00
        AX_PARAM2 = 0x08
        AX_PARAM3 = 0x2F
        CHECKSUM = compute_checksum(bytes((ID, PK_LENGTH, AX_WRITE, AX_PARAM1, AX_PARAM2, AX_PARAM3)))
        
        sc.flush()
        sc.send(bytes((AX_HEADER, AX_HEADER, ID, PK_LENGTH, AX_WRITE, AX_PARAM1, AX_PARAM2, AX_PARAM3, CHECKSUM)))
        print("instruction packet sent... wait 5 seconds")
        time.sleep(5)
        print("Available Dxl are")
        print(getAvailableDxl())


def setID(CURRENT_ID, NEW_ID):
    AX_HEADER = 0xFF
    ID = CURRENT_ID #254 will send to all dynamixels plugged in
    PK_LENGTH = 0x04
    AX_WRITE = 0x03
    AX_PARAM1 = 0x03
    AX_PARAM2 = NEW_ID
    CHECKSUM = compute_checksum(bytes((ID, PK_LENGTH, AX_WRITE, AX_PARAM1, AX_PARAM2))) 
    
    sc.flush()
    sc.send(bytes((AX_HEADER, AX_HEADER, ID, PK_LENGTH, AX_WRITE, AX_PARAM1, AX_PARAM2, CHECKSUM)))
    print("Setting dynamixel ID to ",NEW_ID,"...")
    time.sleep(1)
    print("Success!")
    for dxl in getAvailableDxl():
            print("Dynamixel with", dxl, "is operational.")

def testJoint(ID):
        moveJoint(ID, 0, 512)
        time.sleep(1)
        moveJoint(ID, -45, 512)
        time.sleep(1)
        moveJoint(ID, -90, 512)
        time.sleep(1)
        moveJoint(ID, 45, 512)
#try:
#print(getAvailableDxl())
jointMode(5)
testJoint(5)
       
#except Exception as e:

#        print(e)
