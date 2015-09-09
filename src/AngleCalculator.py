#! /usr/bin/env python

import numpy as np
from sklearn.decomposition import PCA
from transformations import euler_from_quaternion
import scipy
import math 
import json
import sys

class AngleMaker:
    """An object to handle the calculation and smoothing of 
    joint angles based off of quaternion data from the kinect sensor. 
    The quaternion data can be fed in from a file or from a live stream and 
    each call to the calculateEulerTheta method will return the smoothed out value. """
    def __init__(self, angleAlphas=None):
        '''
        Parameterized the alpha values for the exponential moving average 
        for each of the angles. They can be passed in at the time of object creation
        or the default values can be used. 
        '''

        if angleAlphas != None and len(angleAlphas) == 8:
            #Use the passed in alpha values
            self.alphas = angleAlphas
        else:
            #Use the default alpha values
            self.alphas = [.5, .5, .5, .5, .5, .5, .5, .5] 
        
        self.smoothed = [0, 0, 0, 0, 0, 0, 0, 0]


    def generateEulerAngles(self, angles):
        '''
        BASE_FRAMES = ['/openni_depth_frame', '/left_shoulder', '/openni_depth_frame', 'right_shoulder']
        FRAMES = [
            'left_shoulder',
            'left_elbow',
            'right_shoulder',
            'right_elbow',
            ]
        '''

        #Get the joint list
        #jointList

        #get the joint rotations
        LS = euler_from_quaternion(angles[0])
        LE = euler_from_quaternion(angles[1])
        RS = euler_from_quaternion(angles[2])
        RE = euler_from_quaternion(angles[3])

        #To figure out all of the modifications to the angles I hand tested everything. Beware when modifying

        #Right Shoulder Angles
        RSY = -1 * RS[0] + math.pi/2
        RSR = -1 * (RS[1] + math.pi/2)
        RSP = RS[2] - math.pi/2
        #Right Elbow
        REP = RE[1]
        #Left Shoulder Angles
        LSY = LS[0] - math.pi/2
        LSR = -1 * (LS[1] - math.pi/2)
        LSP = -1 * (LS[2] - math.pi/2)
        #Left Elbow
        LEP = -1*LE[1]


        #REP, LEP, RSY, LSY, RSR, LSR, RSP, LSP = self.smooth([REP, LEP, RSY, LSY, RSR, LSR, RSP, LSP])
        
        print [REP, LEP, RSY, LSY, RSR, LSR, RSP, LSP]

        return [REP, LEP, RSY, LSY, RSR, LSR, RSP, LSP]


    def smooth(self, angleList):
        '''
        Smooth out all of the angles and return the list of them 
        '''
        updatedAngles = map(doSmoothing, angleList, self.alphas, self.smoothed)
        self.smoothed = updatedAngles
        return tuple(updatedAngles)



def doSmoothing(newVal, alpha, oldVal):
    '''
    Perform exponential smoothing and some simple flitering
    '''
    if math.fabs(newVal) >= math.pi:
        return oldVal

    return alpha * newVal + (1-alpha) * oldVal


'''
Calculate the theta between two vectors a, and b. 
'''
def calculateTheta(a, b):
    dotProd = np.dot(a, b)        #a dot b
    aNorm = np.sqrt(np.dot(a, a))  # ||a||
    bNorm = np.sqrt(np.dot(b, b))  # ||b||
    #theta = arccos(a dot b / (||a||*||b||))
    val =  dotProd/(aNorm*bNorm)
    #I think there is a float issue
    if val > 1:
        val = 1
    elif val < -1:
        val = -1
    return math.acos(val)


'''
Takes a list of xyz positions for two points, A and
B and generates the vector from A to B
'''
def generateVector(Apos, Bpos):
    #B minus A
    xComp = Bpos[0] - Apos[0]
    yComp = Bpos[1] - Apos[1]
    zComp = Bpos[2] - Apos[2]
    return np.array([xComp, yComp, zComp])


'''
Return a numpy vector of the coordinates for
the joint struture passed to to
'''
def getPointFromJoint(joint):
    posList = []
    posList.append(joint['pos']['x'])
    posList.append(joint['pos']['y'])
    posList.append(joint['pos']['z'])
    return np.array(posList)

'''
Return a numpy vector of the coordinates for
the joint struture passed to to
'''
def getRotFromJoint(joint):
    rotList = []
    rotList.append(joint['rot']['w'])
    rotList.append(joint['rot']['x'])
    rotList.append(joint['rot']['y'])
    rotList.append(joint['rot']['z'])

    return np.array(rotList)


def normalizeVector(vec):
    vec = vec / np.linalg.norm(vec)
    return vec

def translateCoordinates(frame, point):
    #Get the original 
    x = frame[0]
    y = frame[1]
    z = frame[2]
    #Translate each vector according to the point. This may not be proper
    newX = x * point
    newY = y * point
    newZ = z * point

    #new coordinates
    return np.array([newX, newY, newZ])




def getFirstDegreeAngles(frame, origin, point):
    '''
    Given the reference frame, an origin point, and a distant point create a polar coordinate 
    system and return the inclination and azimuth angles. 
    '''
    #Might need to translate the frame first to get the new u
    #Trying my own translation

    #newFrame = translateCoordinates(frame, origin)

    #Calculate the vector from the origin to the point, 
    # the inclentation is the angle between u and that vector

    limb = generateVector(origin, point)
    u = frame[0]
    inclination = calculateTheta(u, limb)

    #Calculate the vector from the origin to the point projected on the plane normal to u
    proj = getProjectedVector(u, limb)
    r = frame[1]
    #vect = generateVector(origin, proj) #Might need to take a second look
    azimuth = calculateTheta(r, proj)

    return (inclination, azimuth)


def getProjectedVector(normal, vector):
    '''
    Project the vector onto the plane defined by the normal vector
    '''
    #http://math.stackexchange.com/questions/633181/formula-to-project-a-vector-onto-a-plane    
    normed = normalizeVector(normal)
    p = np.dot(vector, normed) * normed
    proj = vector - p
    return proj


def getSecondDegreeAngles(frame, shoulder, origin, point): 
    '''
    Get the angles for the second degree joints
    '''
    #Translate the coordinate frame
    #newFrame = translateCoordinates(frame, origin)
    #Create the b vector and the elbow hand vector
    b = -1 * normalizeVector(generateVector(origin, shoulder))
    vect = generateVector(origin, point)
    #Find the inclination angle
    inclination = calculateTheta(b, vect)
    
    #Create rp and the vector le, lhp 
    r = frame[1]
    rp = getProjectedVector(b, r)
    proj = getProjectedVector(b, vect)
    #Find the azimuth
    azimuth = calculateTheta(rp, proj)

    return (inclination, azimuth)





'''
Based off of work found in Real-Time Classification of Dance gestures from Skeleton Animation, 

Represents the joint in a different type of skeletal representation. 

'''
def generateAngles(jsonString):
    #Get the joint values from the string
    jointDict = json.loads(jsonString)

    '''
        JOINTS = [
       0 'head',
       1 'neck',
       2 'torso',
       3 'left_shoulder',
       4 'left_elbow',
       5 'left_hand',
       6 'left_hip',
       7 'left_knee',
       8 'left_foot',
       9 'right_shoulder',
       10 'right_elbow',
       11 'right_hand',
       12 'right_hip',
       13 'right_knee',
       14 'right_foot'
        ]
    '''

    #Get the 7 torso joint positions and place them in a matrix
    #Get the joint list
    jointList = jointDict["Joints"]

    #get the joint rotations
    RS = euler_from_quaternion(getRotFromJoint(jointList[9]))
    LS = euler_from_quaternion(getRotFromJoint(jointList[3]))
    RE = euler_from_quaternion(getRotFromJoint(jointList[10]))
    LE = euler_from_quaternion(getRotFromJoint(jointList[4]))

    RSY = RE[1]
    RSP = RS[1]
    RSR = -1 * RS[2]
    REP = RE[2] #Rotation about Y
    LSY = LE[1]
    LSP = LS[1]
    LSR = LS[2] #Rotation about Z
    LEP = LE[2]

    print [REP, LEP, RSY, LSY, RSR, LSR, RSP, LSP]


    return [REP, LEP, RSY, LSY, RSR, LSR, RSP, LSP]




 

if __name__ == '__main__':
    #If ran alone try to convert a file containing json strings
    # of the appropriate data to a file of angle arrays
    filename = "Positions.log"
    output = "JointAngles.txt"

    if len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 3:
        output = sys.argv[2]
    elif len(sys.argv) > 3:
        print "Usage: ./AngleCalculator.py <Input File> <Output File>"

    #Open the input file
    fIn = open(filename, 'r')
    #Open the output file
    fOut = open(output, 'w')
    #Iterate through line by line of the input
    #creating a row vector for each line in the output
    for line in fIn:
        vector = generateAngles(line)
        fOut.write(str(vector) + "\n")
