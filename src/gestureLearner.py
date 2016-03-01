#!/usr/bin/env python
# encoding: utf-8


"""
Learn gestures from the kinect by recording key frame positions from user input. This 
is just the foundation of some potential work I might look into. 

Author: Ryan
ITERO's original project used the Kinect V2 that only ran on windows. This
uses a regular kinect or asus xtion pro and runs entirely on linux.  
"""

import signal
import numpy as np
import AngleCalculator 
import time

import socket
TCP_IP = "192.168.0.110"
TCP_PORT = 7238


sock = socket.socket(socket.AF_INET, #Internet 
                     socket.SOCK_STREAM) #TCP
sock.bind((TCP_IP, TCP_PORT))

continuing = True


class gestureMaker:
    def __init__(self, outputFile="./data/out.txt"):
        #The output script that this will make
        self.output = open(outputFile, 'w')
        #Create the angle maker object to calculate the angles from the kinect data
        self.angleMaker = AngleMaker()

        #Set up for the output script
        self.output.write("#!/usr/bin/env python \n")
        self.output.write("from Maestor import maestor\n\n")
        self.output.write("if __name__ == \'__main__\':\n")
        self.output.write("    robot = maestor()\n\n")
    

    def recordJointAngles(self):

        # #Get the values from the kinect
        # values = self.kinect.get_posture()
        # if values is None:
        #     #recursivly try again
        #     self.recordJointAngles()
        #     return None

        #Get values from the windows 

        #Getting data from the socket:
        line = conn.recv(4096) #buffer size is 4096 bytes
        if not line:
            return # No line, do nothing
        print "Read a good line"

        #Uses matt's code
        stringNums = calculateAngles(line)


        self.output.write("    robot.setProperties(\"REP LEP RSY LSY RSR LSR RSP LSP\", \"position position position position position position position position\", \"" + stringNums + "\")\n")
        self.output.write("    robot.waitForJointList([\"REP\", \"LEP\", \"RSY\", \"LSY\", \"RSR\", \"LSR\", \"RSP\", \"LSP\"])\n")


    def cleanUp(self):
        #Close the file 
        self.output.close()



def endDemo(signal, frame):
    global continuing
    continuing = False

def main():
    global continuing
    signal.signal(signal.SIGINT, endDemo)
    #Create a recorder and record a line of positions each time a key is pressed.
    recorder = gestureMaker()
    while continuing:
        response = raw_input("Press any key to continue or q to quit")
        if response == "q":
            continuing = False
            continue
        #Add another line
        recorder.recordJointAngles()

    recorder.cleanUp()


if __name__ == '__main__':
    main()

 

