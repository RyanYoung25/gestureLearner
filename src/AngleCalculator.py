'''
Pieced together code from Matt's star project. Needs to be cleaned up but we're on a schedule. 
'''

import re
import math 
import time

pi = 3.1415926
#initializing the filtering algorithm: (uses moving average)
alpha = 0.3 #alpha for filtering

newREO_prev = 0

newLEO_prev = 0

newRightElbowTheta_prev = 0

newLeftElbowTheta_prev = 0

newRightShoulderTheta_prev = 0

newLeftShoulderTheta_prev = 0

#Making a cross product function to make life easier:
def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c

#Making a norm function to make life easier:
def norm(a):
    c = math.sqrt(a[0]**2 + a[1]**2 + a[2]**2)

    return c

#Making a component wise division function to make like easier:
def compdev(a,b):
    for i in range(0,len(a)):
        a[i] = a[i]/b

    return a

    #Making a component wise division function to make like easier:
def compadd(a,b):
    for i in range(0,len(a)):
        a[i] = a[i]+b

    return a

def vectadd(a,b):
    c = [a[0] + b[0], a[1] + b[1], a[2] + b[2]]

    return c

def calculateAngles(line):
    #Initizaling a bunch of arrays for later concatination:
        RWX = [] #Right Wrist 
        RWY = []
        RWZ = []
        LWX = [] #Left Wrist
        LWY = []
        LWZ = []

        REX = [] #Right Elbow
        REY = []
        REZ = []
        LEX = [] #Left Elbow
        LEY = []
        LEZ = []

        RSX = [] #Right Shoulder
        RSY = []
        RSZ = []
        LSX = [] #Left Shoulder
        LSY = []
        LSZ = []

        SSX = [] #SPINE Shoulder
        SSY = []
        SSZ = []

        RHX = [] #Right HIP
        RHY = []
        RHZ = []
        LHX = [] #Left HIP
        LHY = []
        LHZ = []

        #using regular expressions to extract the data in the text file from the kinect socket
        
        RWX.append(re.findall(r'RWX:[-]*\d.\d+', line)[0]) 
        RWY.append(re.findall(r'RWY:[-]*\d.\d+', line)[0])
        RWZ.append(re.findall(r'RWZ:[-]*\d.\d+', line)[0])
        LWX.append(re.findall(r'LWX:[-]*\d.\d+', line)[0])
        LWY.append(re.findall(r'LWY:[-]*\d.\d+', line)[0])
        LWZ.append(re.findall(r'LWZ:[-]*\d.\d+', line)[0])


        REX.append(re.findall(r'REX:[-]*\d.\d+', line)[0])
        REY.append(re.findall(r'REY:[-]*\d.\d+', line)[0])
        REZ.append(re.findall(r'REZ:[-]*\d.\d+', line)[0])
        LEX.append(re.findall(r'LEX:[-]*\d.\d+', line)[0])
        LEY.append(re.findall(r'LEY:[-]*\d.\d+', line)[0])
        LEZ.append(re.findall(r'LEZ:[-]*\d.\d+', line)[0])

        RSX.append(re.findall(r'RSX:[-]*\d.\d+', line)[0])
        RSY.append(re.findall(r'RSY:[-]*\d.\d+', line)[0])
        RSZ.append(re.findall(r'RSZ:[-]*\d.\d+', line)[0])
        LSX.append(re.findall(r'LSX:[-]*\d.\d+', line)[0])
        LSY.append(re.findall(r'LSY:[-]*\d.\d+', line)[0])
        LSZ.append(re.findall(r'LSZ:[-]*\d.\d+', line)[0])

        SSX.append(re.findall(r'SSX:[-]*\d.\d+', line)[0])
        SSY.append(re.findall(r'SSY:[-]*\d.\d+', line)[0])
        SSZ.append(re.findall(r'SSZ:[-]*\d.\d+', line)[0])

        RHX.append(re.findall(r'RHX:[-]*\d.\d+', line)[0])
        RHY.append(re.findall(r'RHY:[-]*\d.\d+', line)[0])
        RHZ.append(re.findall(r'RHZ:[-]*\d.\d+', line)[0])
        LHX.append(re.findall(r'LHX:[-]*\d.\d+', line)[0])
        LHY.append(re.findall(r'LHY:[-]*\d.\d+', line)[0])
        LHZ.append(re.findall(r'LHZ:[-]*\d.\d+', line)[0])


        #Removing letters and turning strings into numbers:
        for i in range(0,len(RWX)):

            
            RWX[i] = RWX[i][4:11] #taking out the "RW:"
            RWX[i] = float(RWX[i]) #converting the string to a number
            
            RWY[i] = RWY[i][4:11] #taking out the "RW:"
            RWY[i] = float(RWY[i]) #converting the string to a number
            
            RWZ[i] = RWZ[i][4:11] #taking out the "RW:"
            RWZ[i] = float(RWZ[i]) #converting the string to a number
            
            LWX[i] = LWX[i][4:11] #taking out the "LW:"
            LWX[i] = float(LWX[i]) #converting the string to a number
            
            LWY[i] = LWY[i][4:11] #taking out the "LW:"
            LWY[i] = float(LWY[i]) #converting the string to a number
            
            LWZ[i] = LWZ[i][4:11] #taking out the "LW:"
            LWZ[i] = float(LWZ[i]) #converting the string to a number
            
            REX[i] = REX[i][4:11] #taking out the "RW:"
            REX[i] = float(REX[i]) #converting the string to a number

            REY[i] = REY[i][4:11] #taking out the "RW:"
            REY[i] = float(REY[i]) #converting the string to a number
            
            REZ[i] = REZ[i][4:11] #taking out the "RW:"
            REZ[i] = float(REZ[i]) #converting the string to a number
            
            LEX[i] = LEX[i][4:11] #taking out the "LW:"
            LEX[i] = float(LEX[i]) #converting the string to a number
            
            LEY[i] = LEY[i][4:11] #taking out the "LW:"
            LEY[i] = float(LEY[i]) #converting the string to a number
            
            LEZ[i] = LEZ[i][4:11] #taking out the "LW:"
            LEZ[i] = float(LEZ[i]) #converting the string to a number
            
            RSX[i] = RSX[i][4:11] #taking out the "RW:"
            RSX[i] = float(RSX[i]) #converting the string to a number

            RSY[i] = RSY[i][4:11] #taking out the "RW:"
            RSY[i] = float(RSY[i]) #converting the string to a number
            
            RSZ[i] = RSZ[i][4:11] #taking out the "RW:"
            RSZ[i] = float(RSZ[i]) #converting the string to a number
            
            LSX[i] = LSX[i][4:11] #taking out the "LW:"
            LSX[i] = float(LSX[i]) #converting the string to a number
            
            LSY[i] = LSY[i][4:11] #taking out the "LW:"
            LSY[i] = float(LSY[i]) #converting the string to a number
            
            LSZ[i] = LSZ[i][4:11] #taking out the "LW:"
            LSZ[i] = float(LSZ[i]) #converting the string to a number
            
            SSX[i] = SSX[i][4:11] #taking out the "LW:"
            SSX[i] = float(SSX[i]) #converting the string to a number
            
            SSY[i] = SSY[i][4:11] #taking out the "LW:"
            SSY[i] = float(SSY[i]) #converting the string to a number
            
            SSZ[i] = SSZ[i][4:11] #taking out the "LW:"
            SSZ[i] = float(SSZ[i]) #converting the string to a number
            
            RHX[i] = RHX[i][4:11] #taking out the "RW:"
            RHX[i] = float(RHX[i]) #converting the string to a number
            
            RHY[i] = RHY[i][4:11] #taking out the "RW:"
            RHY[i] = float(RHY[i]) #converting the string to a number
            
            RHZ[i] = RHZ[i][4:11] #taking out the "RW:"
            RHZ[i] = float(RHZ[i]) #converting the string to a number
            
            LHX[i] = LHX[i][4:11] #taking out the "LW:"
            LHX[i] = float(LHX[i]) #converting the string to a number
            
            LHY[i] = LHY[i][4:11] #taking out the "LW:"
            LHY[i] = float(LHY[i]) #converting the string to a number
            
            LHZ[i] = LHZ[i][4:11] #taking out the "LW:"
            LHZ[i] = float(LHZ[i]) #converting the string to a number


        #Initializing Values:
        RightElbowTheta = [] #Angle between right elbow pitch
        LeftElbowTheta = []  #Angle between left elbow pitch   
        LeftShoulderTheta = [] #Left shoulder Roll
        RightShoulderTheta = [] #Right Shoulder Roll
        REOTheta = [] #Right Shoulder Yaw
        LEOTheta = [] #Left Shoulder Yaw

        #initiaizing filtered shtuff:
        filteredREOTheta = []

        filteredLEOTheta = []

        filteredRightElbowTheta = []

        filteredLeftElbowTheta = []

        filteredRightShoulderTheta = []

        filteredLeftShoulderTheta = []





        for i in range(0,len(RWX)):

            #finding RIGHT elbow angle 
            a = [RWX[i]-REX[i], RWY[i]-REY[i], RWZ[i]-REZ[i]] 
            b = [RSX[i]-REX[i], RSY[i]-REY[i], RSZ[i]-REZ[i]]
            adotb = ((RWX[i]-REX[i])*(RSX[i]-REX[i]) + (RWY[i]-REY[i])*(RSY[i]-REY[i]) +(RWZ[i]-REZ[i])*(RSZ[i]-REZ[i]))
            maga = math.sqrt( (RWX[i]-REX[i])**2 + (RWY[i]-REY[i])**2 + (RWZ[i]-REZ[i])**2) 
            magb = math.sqrt( (RSX[i]-REX[i])**2 + (RSY[i]-REY[i])**2 + (RSZ[i]-REZ[i])**2 )
            RightElbowTheta.append(math.acos( (adotb)/(maga*magb) ) )
            REO = cross(a,b)
            #disp(REO)

            #SMOOTHING
            newRightElbowTheta = RightElbowTheta[-1] #Set the new Right elbow theta to the last calculated theta #math.acos( (adotb)/(maga*magb) ) 
            newRightElbowTheta = ((alpha)*newRightElbowTheta + (1-alpha)*newRightElbowTheta_prev)
            filteredRightElbowTheta.append( newRightElbowTheta ) 
            newRightElbowTheta_prev =  newRightElbowTheta

            #finding z line cross shoulder elbow vector:
            avec = [REX[i], REY[i], 2] 
            bvec = [RSX[i]-REX[i], RSY[i]-REY[i], RSZ[i]-REZ[i]]
            zcrossRS = cross(avec, bvec) 
            #finding cross of zcrossR and bvec
            RScrosszcrossRS= cross(bvec, zcrossRS)

            #finding z line cross shoulder elbow vector:
            avec1 = [LEX[i], LEY[i], 2] 
            bvec1 = [LSX[i]-LEX[i], LSY[i]-LEY[i], LSZ[i]-LEZ[i]]
            zcrossLS = cross(avec1, bvec1)
            #finding cross of zcrossR and bvec
            LScrosszcrossLS = cross(bvec1, zcrossLS)    

            #finding LEFT elbow angle
            a1 = [LWX[i]-LEX[i], LWY[i]-LEY[i], LWZ[i]-LEZ[i]]
            b1 = [LSX[i]-LEX[i], LSY[i]-LEY[i], LSZ[i]-LEZ[i]]
            a1dotb1 = (LWX[i]-LEX[i])*(LSX[i]-LEX[i]) + (LWY[i]-LEY[i])*(LSY[i]-LEY[i]) +(LWZ[i]-LEZ[i])*(LSZ[i]-LEZ[i])
            maga1 = math.sqrt( (LWX[i]-LEX[i])**2 + (LWY[i]-LEY[i])**2 + (LWZ[i]-LEZ[i])**2 )
            magb1 = math.sqrt( (LSX[i]-LEX[i])**2 + (LSY[i]-LEY[i])**2 + (LSZ[i]-LEZ[i])**2 )
            LeftElbowTheta.append( math.acos( (a1dotb1)/(maga1*magb1)  ) ) 
            LEO = cross(b1,a1)

            #SMOOOTHING
            newLeftElbowTheta = math.acos( (a1dotb1)/(maga1*magb1) ) 
            newLeftElbowTheta = ((alpha)*newLeftElbowTheta + (1-alpha)*newLeftElbowTheta_prev) 
            filteredLeftElbowTheta.append( newLeftElbowTheta ) 
            newLeftElbowTheta_prev =  newLeftElbowTheta


            #finding left shoulder angle :
            a2dotb2 = (LHX[i]-LSX[i])*(LEX[i]-LSX[i]) + (LHY[i]-LSY[i])*(LEY[i]-LSY[i]) + (LHZ[i]-LSZ[i])*(LEZ[i] -LSZ[i])
            maga2 = math.sqrt(  (LHX[i]-LSX[i])**2 +  (LHY[i]-LSY[i])**2 +  (LHZ[i]-LSZ[i])**2 )
            magb2 = math.sqrt( (LEX[i]-LSX[i])**2 + (LEY[i]-LSY[i])**2 + (LEZ[i] -LSZ[i])**2 )
            LeftShoulderTheta.append( math.acos( (a2dotb2)/(maga2*magb2) ) ) 
           
           #SMOOOTHING
            newLeftShoulderTheta = math.acos( (a2dotb2)/(maga2*magb2) ) 
            newLeftShoulderTheta = ((alpha)*newLeftShoulderTheta + (1-alpha)*newLeftShoulderTheta_prev)
            filteredLeftShoulderTheta.append( newLeftShoulderTheta) 
            newLeftShoulderTheta_prev =  newLeftShoulderTheta


            #finding right shoulder angle:
            a3dotb3 = (RHX[i]-RSX[i])*(REX[i]-RSX[i]) + (RHY[i]-RSY[i])*(REY[i]-RSY[i]) +(RHZ[i]-RSZ[i])*(REZ[i]-RSZ[i])
            maga3 = math.sqrt( (REX[i]-RSX[i])**2 + (REY[i]-RSY[i])**2 + (REZ[i]-RSZ[i])**2  )
            magb3 = math.sqrt( (RHX[i]-RSX[i])**2 + (RHY[i]-RSY[i])**2 + (RHZ[i]-RSZ[i])**2 )
            RightShoulderTheta.append( math.acos( (a3dotb3)/(maga3*magb3) ) )

            #SMOOOTHING
            newRightShoulderTheta = math.acos( (a3dotb3)/(maga3*magb3) ) 
            newRightShoulderTheta = ((alpha)*newRightShoulderTheta + (1-alpha)*newRightShoulderTheta_prev) 
            filteredRightShoulderTheta.append( newRightShoulderTheta ) 
            newRightShoulderTheta_prev =  newRightShoulderTheta



            #calculating position of REO
            RE = [REX[i], REY[i], REZ[i]]
            LE = [LEX[i], LEY[i], LEZ[i]]
            #REO = [REO[0] REO[1] REO[2]] #This is the full elbow orientation data
            REO = [REO[0], REO[1], REO[2]]
            #REO = (REO / norm(REO)) + RE # REO = [REOX REOY REOZ]
            step1REO = compdev(REO, norm(REO))
            REO = vectadd(step1REO, RE)

            #zcrossRS = (zcrossRS / norm(zcrossRS)) + RE
            step1zcrossRS = compdev(zcrossRS, norm(zcrossRS))
            zcrossRS = vectadd(step1zcrossRS, RE)

            #RScrosszcrossRS = (RScrosszcrossRS / norm(RScrosszcrossRS)) + RE
            step1RScrosszcrossRS = compdev(RScrosszcrossRS,norm(RScrosszcrossRS))
            RScrosszcrossRS = vectadd(step1RScrosszcrossRS, RE)



            LEO = [LEO[0], LEO[1], LEO[2]]
            #LEO = (LEO / norm(REO)) + LE # LEO = [LEOX LEOY LEOZ]
            step1LEO = compdev(LEO, norm(LEO))
            LEO = vectadd(step1LEO, LE)

            #zcrossLS = (zcrossLS / norm(zcrossLS)) + LE
            step1zcrossLS = compdev(zcrossLS, norm(zcrossLS))
            zcrossLS = vectadd(step1zcrossLS, LE)

            #LScrosszcrossLS = (LScrosszcrossLS / norm(LScrosszcrossLS)) + LE
            step1LScrosszcrossLS = compdev(LScrosszcrossLS,norm(LScrosszcrossLS))
            LScrosszcrossLS = vectadd(step1LScrosszcrossLS, LE)

            #Finding angle between horizontal and REO
            REHo = [REX[i], REY[i], .5] 
            a4dotb4 = (REO[0]- REX[i])*(RScrosszcrossRS[0]-REX[i]) + (REO[1]- REY[i])*(RScrosszcrossRS[1]-REY[i])+(REO[2]- REZ[i])*(RScrosszcrossRS[2]-REZ[i])
            maga4 = math.sqrt(  (RScrosszcrossRS[0]-REX[i])**2 +  (RScrosszcrossRS[1]-REY[i])**2    +(RScrosszcrossRS[2]-REZ[i])**2  )
            magb4 = math.sqrt( (REO[0]- REX[i])**2 +  (REO[1]- REY[i])**2 + (REO[2]- REZ[i])**2)
            REOTheta.append( math.acos( (a4dotb4)/(maga4*magb4) ) - 1.57 ) 
            #disp(REOTheta[i])

            newREO = math.acos( (a4dotb4)/(maga4*magb4) ) - 1.57 
            newREO = ((alpha)*newREO + (1-alpha)*newREO_prev)
            filteredREOTheta.append( (newREO) ) 
            newREO_prev =  newREO 

            #Finding angle between horizontal and LEO
            LEHo = [LEX[i], LEY[i], .5] 
            a5dotb5 = (LEO[0]- LEX[i])*(LScrosszcrossLS[0]-LEX[i]) + (LEO[1]- LEY[i])*(LScrosszcrossLS[1]-LEY[i])+(LEO[2]- LEZ[i])*(LScrosszcrossLS[2]-LEZ[i])
            maga5 = math.sqrt(  (LScrosszcrossLS[0]-LEX[i])**2 +  (LScrosszcrossLS[1]-LEY[i])**2    +(LScrosszcrossLS[2]-LEZ[i])**2  )
            magb5 = math.sqrt( (LEO[0]- LEX[i])**2 +  (LEO[1]- LEY[i])**2 + (LEO[2]- LEZ[i])**2)
            LEOTheta.append( -1*(math.acos( (a5dotb5)/(maga5*magb5) ) - 1.57) ) 
            #disp(LEOTheta[i])

            newLEO = -1*(math.acos( (a5dotb5)/(maga5*magb5) ) - 1.57)
            newLEO = ((alpha)*newLEO + (1-alpha)*newLEO_prev)
            filteredLEOTheta.append( (newLEO) ) 
            newLEO_prev =  newLEO



        #making adjusted angles (angles that hubo plays nice with):
        ADJRightElbowTheta = []
        ADJLeftElbowTheta = []
        ADJRightShoulderTheta = []
        ADJLeftShoulderTheta = []

        filteredADJRightElbowTheta = []
        filteredADJLeftElbowTheta = []
        filteredADJRightShoulderTheta = []
        filteredADJLeftShoulderTheta = []

        #Adjusting angle offsets
        for i in range(0,len(RightElbowTheta)):
           
            ADJRightElbowTheta.append(RightElbowTheta[i]  - pi )
            ADJLeftElbowTheta.append(LeftElbowTheta[i] - pi)
            ADJRightShoulderTheta.append(-1*(RightShoulderTheta[i] - .4) )
            ADJLeftShoulderTheta.append(LeftShoulderTheta[i] - .4) 

            filteredADJRightElbowTheta.append(filteredRightElbowTheta[i]  - pi )
            filteredADJLeftElbowTheta.append(filteredLeftElbowTheta[i] - pi)
            filteredADJRightShoulderTheta.append(-1*(filteredRightShoulderTheta[i] - .4) )
            filteredADJLeftShoulderTheta.append(filteredLeftShoulderTheta[i] - .4) 


            

        for i in range(0,len(ADJRightElbowTheta)):
            
            if ADJRightElbowTheta[i] < -2 :  #Fixing if you go out of bounds of the robot
                ADJRightElbowTheta[i] = -2
            
            if ADJRightElbowTheta[i] > 0  : #Fixing if you go out of bounds of the robot
                ADJRightElbowTheta[i] = 0
            if ADJLeftElbowTheta[i] < -2 :
                ADJLeftElbowTheta[i] = -2
            if ADJLeftElbowTheta[i] > 0 :
                ADJLeftElbowTheta[i] = 0
           
            if ADJRightShoulderTheta[i] < -2.5 :
                ADJRightShoulderTheta[i] = -2.5
            if ADJRightShoulderTheta[i] > 0  :
                ADJRightShoulderTheta[i] = 0
            
            if ADJLeftShoulderTheta[i] > 2.5 :
                ADJLeftShoulderTheta[i] = 2.5
            if ADJLeftShoulderTheta[i] < 0 :
               ADJLeftShoulderTheta[i] = 0 
            
            if filteredREOTheta[i] < -2.25 :
                filteredREOTheta[i] = -2.25
            if filteredREOTheta[i] > 2.25 :
                filteredREOTheta[i] = 2.25
            
            if filteredLEOTheta[i] < -2.25 :
                filteredLEOTheta[i] = -2.25
            if filteredLEOTheta[i] > 2.25 :
                filteredLEOTheta[i] = 2.25

            return str(round(filteredADJRightElbowTheta[0],2)) +" "+ str(round(filteredADJLeftElbowTheta[0],2)) +" "+ str(round(filteredADJRightShoulderTheta[0],2)) +" "+ str(round(filteredADJLeftShoulderTheta[0],2)) +" "+ str(round(filteredREOTheta[0],2)) +" "+ str(round(filteredLEOTheta[0],2))