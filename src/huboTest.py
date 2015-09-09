#!/usr/bin/env python
from Maestor import maestor
from AngleCalculator import AngleMaker
import sys
from ast import literal_eval 



'''
This is a test case where it reads in the input file of json strings and runs the 
calculated angles on the robot in simulation. 
'''


def readAndMove(FileName, robot):
    '''
    Open the file then for each line calculate the angles and push them to hubo
    '''
    try:
        

        f = open(FileName)
        count = 0
        anglemaker = AngleMaker()

        for dataString in f:
            if count % 10 == 0:
                #Generate the angles from the string
                angleList = literal_eval(dataString)
                angles = anglemaker.generateEulerAngles(angleList)

                #Create a string of the angle values
                stringNums = ""
                for angle in angles:
                    stringNums += str(angle) + " "

                #Remove the last space
                stringNums = stringNums[:-1]

                #Send the command to the robot
                robot.setProperties("REB LEB RSY LSY RSR LSR RSP LSP", "position position position position position position position position", stringNums)
            count += 1 

        robot.setProperties("REB LEB RSY LSY RSR LSR RSP LSP", "position position position position position position position position", "0 0 0 0 0 0 0 0")

    except Exception, e:
        print "An error occurred"
        print e


def main():

    if len(sys.argv) == 2:
        robot = maestor()
        readAndMove(sys.argv[1], robot)
    else:
        print "Usage: huboTest.py <FileName>"
        print "FileName must be the path to a file with the correct json string format"
        print "Exiting..."
        sys.exit(-1)

if __name__ == '__main__':
    main()
