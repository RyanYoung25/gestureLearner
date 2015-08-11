#! /usr/bin/env python

import numpy as np
from sklearn.decomposition import PCA
import scipy
import math 
import json
import sys

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

    #get the joints
    RS = getPointFromJoint(jointList[9])
    NK = getPointFromJoint(jointList[1])
    LS = getPointFromJoint(jointList[3])
    TS = getPointFromJoint(jointList[2])
    RH = getPointFromJoint(jointList[12])
    LH = getPointFromJoint(jointList[6])

    #Get more joints
    LE = getPointFromJoint(jointList[4])
    RE = getPointFromJoint(jointList[10]) 
    LW = getPointFromJoint(jointList[5])
    RW = getPointFromJoint(jointList[11]) 
    
    #Create the matrix
    torso = np.array([RS, NK, LS, TS, RH, LH])

    #Create the pca object and fit it to the torso to get the coordinate frame. 
    pca = PCA(n_components=2)
    pca.fit(torso)


    #Create the torso frame
    # {u, r, t} is the torso frame
    u = pca.components_[0]
    r = pca.components_[1]
    t = np.cross(u, r)

    frame = np.array([u, r, t])


    LSR, LSP = getFirstDegreeAngles(frame, LS, LE)

    RSR, RSP = getFirstDegreeAngles(frame, RS, RE)

    LEP, LSY = getSecondDegreeAngles(frame, LS, LE, LH)

    REP, RSY = getSecondDegreeAngles(frame, RS, RE, RH)

    return [RSP, LSP, RSR, LSR, RSY, LSY, REP, LEP]
 










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
