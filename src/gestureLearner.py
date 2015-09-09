#!/usr/bin/env python
# encoding: utf-8


"""
Learn gestures from the kinect by recording key frame positions from user input. This 
is just the foundation of some potential work I might look into. 

Author: Ryan
ITERO's original project used the Kinect V2 that only ran on windows. This
uses a regular kinect or asus xtion pro and runs entirely on linux.  

The kinect class was authored by: omangin
"""


import roslib
roslib.load_manifest('gestureLearner')
import rospy
import tf
import signal
import numpy as np
from jsonConverter import jsonMaker, jointLineMaker
from AngleCalculator import generateEulerAngles
import time

BASE_FRAMES = ['/openni_depth_frame', '/left_shoulder_', '/openni_depth_frame', 'right_shoulder_']
FRAMES = [
        'left_shoulder',
        'left_elbow',
        'right_shoulder',
        'right_elbow',
        ]
LAST = rospy.Duration()

continuing = True




class Kinect:

    def __init__(self, user=1):
        rospy.init_node("Itero", anonymous=True)
        self.listener = tf.TransformListener()
        self.user = user

        BASE_FRAMES[1] += str(self.user)
        BASE_FRAMES[3] += str(self.user)
    
    def get_posture(self):
        """Returns a list of frames constituted by a translation matrix
        and a rotation matrix.

        Raises IndexError when a frame can't be found (which happens if
        the requested user is not calibrated).
        """
        try:
            frames = []
            for index in range(0,len(FRAMES)):
                #Block until there are enough tf frames in the buffer
                self.listener.waitForTransform(BASE_FRAMES[index], "/%s_%d" % (FRAMES[index], self.user), rospy.Time(0), rospy.Duration(4.0))

                trans, rot = self.listener.lookupTransform(BASE_FRAMES[index],"/%s_%d" % (FRAMES[index], self.user), rospy.Time(0))

                frames.append(rot)
            return frames
        except (tf.LookupException):
            print "User: " + str(self.user) + " not in frame"
        except (tf.ConnectivityException):
            print "Connectivity Exception"
        except (tf.ExtrapolationException):
            print "ExtrapolationException"
        except tf.Exception, e:
            print e
            print "You done goofed"

class DataRecorder:
    def __init__(self, angleFile="./data/angle.txt", positionFile="./data/pos.txt", dataFile="./data/data2.txt"):
        #Wait for the service we want before we publish
        #[REB LEB RSY LSY RSR LSR RSP LSP]
        # Each of these arrays are values for each joint that it matches up with
        #Used for smoothing
        #Getting the angles and publishing to hubo
        self.kinect = Kinect()
        # self.angles = open(angleFile, 'w')
        # self.position = open(positionFile, 'w')
        self.data = open(dataFile, 'w')
    

    def recordJointAngles(self):

        #Get the values from the kinect
        values = self.kinect.get_posture()
        if values is None:
            #recursivly try again
            self.recordJointAngles()
            return None

        #Make them into angles
        angles = generateEulerAngles(values)

        # #Parse angles
        # stringNums = ""
        # for angle in angles:
        #     stringNums += str(angle) + " "

        # stringNums = stringNums[:-1]

        # posString = jointLineMaker((values,))

        self.angles.write(stringNums + "\n")
        #self.position.write(posString + "\n")
        self.data.write(str(values) + "\n")


    def cleanUp(self):
        #Close the file 
        # self.angles.close()
        # self.position.close()
        self.data.close()



def endDemo(signal, frame):
    global continuing
    continuing = False

def main():
    global continuing
    signal.signal(signal.SIGINT, endDemo)
    logger = DataRecorder()
    while continuing:
        logger.recordJointAngles()
    logger.cleanUp()


if __name__ == '__main__':
    main()

 

