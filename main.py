from sa import SA
from individual import Individual
import random

class Main:
    maxIterationNum = 100 #best fitness = -2278 
    trafficLightNum = 4

if  __name__== "__main__":
    #fix random
    random.seed(1)
    #construct a start individual
    dataDir = "sumo/SampleRoad/" + "Caltrain/"
    #dataDir = "sumo/SampleRoad/" + "GridLocalOptimum/"
    ins = SA(Main.maxIterationNum, Main.trafficLightNum)
    startIndividual = Individual.generateRandomIndividual(Main.trafficLightNum)
    ins.startSA(dataDir, startIndividual)
    print ("Process done!")

