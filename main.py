from sa import SA
from individual import Individual
import random


if  __name__== "__main__":
    #fix random
    random.seed(1)
    #construct a start individual
    dataDir = "sumo/SampleRoad/" + "Caltrain/"
    maxIterationNum = 100 
    trafficLightNum = 4
    ins = SA()
    startIndividual = Individual.generateRandomIndividual(trafficLightNum)
    ins.startSA(dataDir, maxIterationNum, trafficLightNum, startIndividual)
    print ("Process done!")

