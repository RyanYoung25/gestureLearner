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
from jsonConverter import jsonMaker
from AngleCalculator import generateAngles
import time

BASE_FRAME = '/openni_depth_frame'
FRAMES = [
        'head',
        'neck',
        'torso',
        'left_shoulder',
        'left_elbow',
        'left_hand',
        'left_hip',
        'left_knee',
        'left_foot',
        'right_shoulder',
        'right_elbow',
        'right_hand',
        'right_hip',
        'right_knee',
        'right_foot',
        ]
LAST = rospy.Duration()

continuing = True




class Kinect:

    def __init__(self, user=1):
        rospy.init_node("Itero", anonymous=True)
        self.listener = tf.TransformListener()
        self.user = user

    
    def get_posture(self):
        """Returns a list of frames constituted by a translation matrix
        and a rotation matrix.

        Raises IndexError when a frame can't be found (which happens if
        the requested user is not calibrated).
        """
        try:
            frames = []
            for frame in FRAMES:
                #Block until there are enough tf frames in the buffer
                self.listener.waitForTransform(BASE_FRAME, "/%s_%d" % (frame, self.user), rospy.Time(0), rospy.Duration(4.0))

                trans, rot = self.listener.lookupTransform(BASE_FRAME,"/%s_%d" % (frame, self.user), rospy.Time(0))

                frames.append((frame, trans, rot))
            return frames
        except (tf.LookupException):
            print "User: " + str(self.user) + " not in frame"
        except (tf.ConnectivityException):
            print "Connectivity Exception"
        except (tf.ExtrapolationException):
            print "ExtrapolationException"
        except (tf.Exception):
            print "You done goofed"

class GestureLearner:
    def __init__(self, fileName="testLog.py"):
        #Wait for the service we want before we publish
        #[REB LEB RSY LSY RSR LSR RSP LSP]
        # Each of these arrays are values for each joint that it matches up with
        #Used for smoothing
        #Getting the angles and publishing to hubo
        self.kinect = Kinect()
        self.output = open(fileName, 'w')

    def setupFile(self):
        #Put in the header and any info in the output file here
        self.output.write("#!/usr/bin/env python")
        self.output.write("from Maestor import maestor")
        self.output.write("\n\n")
        self.output.write("if __name__ == __main__:")
        self.output.write("    robot = maestor()")
    

    def recordJointAngles(self):

        #Get the values from the kinect
        values = self.kinect.get_posture()
        if values is None:
            #recursivly try again
            self.recordJointAngles()
            return None

        angleString = jsonMaker((values,))
        #Make them into angles
        angles = generateAngles(angleString)

        #Parse angles
        stringNums = ""
        for angle in angles:
            stringNums += str(angle) + " "

        stringNums = stringNums[:-1]

        #Write the angles to a file
        self.output.write("    robot.setProperties(\"REP LEP RSY LSY RSR LSR RSP LSP\", \"position position position position position position position position\", " + stringNums + ")")

    def cleanUp(self):
        #Close the file 
        self.output.close()



def endDemo(signal, frame):
    global continuing
    continuing = False

def main():
    signal.signal(signal.SIGINT, endDemo)
    logger = GestureLearner()
    while continuing:
        raw_input("Press enter to record a keyframe, otherwise ctrl-c to write the script")
        logger.recordJointAngles()
    logger.cleanUp()


if __name__ == '__main__':
    main()

 

