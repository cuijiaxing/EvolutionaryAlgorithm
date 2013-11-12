from sa import SA
from individual import Individual



if  __name__== "__main__":
    #construct a start individual
    maxIterationNum = 200 
    trafficLightNum = 4
    ins = SA()
    startIndividual = Individual.generateRandomIndividual(trafficLightNum)
    ins.startSA(maxIterationNum, trafficLightNum, startIndividual)
    print ("Process done!")

