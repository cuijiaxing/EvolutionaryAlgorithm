from simulate import Simulate
import math
import random

class SA:

    def __init__(self):
        #do nothing
        pass

    def temperature(self, currentTime, totalTime):
        return totalTime - currentTime
    
    def P(self, prevIndividual, individual, time):
        
        #always accept better ones
        if individual.fitness > prevIndividual.fitness:
            return 1
        else:
            delta = prevIndividual.fitness - individual.fitness
            return 1 / (1 + math.exp(delta * 1.0 / time))
        
        
        
            




    def iterate(self, maxIterationNum, startIndividual):
        #define best individual and best energy
        bestIndividual = None;
        #define current individual and current energy
        bestEnergy = currentEnergy = 0 
        currentIndividual = None
        timeCount = 1 #it has to be at 1 because in temperature function ,it is a denomerator 
        #define the optimal fitness the system can achieve
        optimalEnergy = 99999999 
        
        #before start, evaluate the start individual first
        startIndividual.evaluate() #get the fitness
        currentIndividual = startIndividual
        currentEnergy = currentIndividual.fitness
        while timeCount < maxIterationNum and currentEnergy < optimalEnergy:
            #get the current temperature
            T = self.temperature(timeCount, maxIterationNum)
            #get the neighbour
            newInd = currentIndividual.neighbour("random")
            newInd.evaluate()
            
            acquiredP = self.P(currentIndividual, newInd, T)
            creterionP = random.random()
            print acquiredP
            print creterionP
            
            if acquiredP > creterionP:
                print "transition success"
                currentIndividual = newInd
                currentEnergy = newInd.fitness
            else:
                print "Transition Failed"
            if newInd.fitness > bestEnergy:
                bestIndividual = newInd
                bestEnergy = newInd.fitness
            timeCount = timeCount + 1
            print currentIndividual.fitness
        
        return bestIndividual
    
    def recordBestToFile(self, fileName, individual, trafficLightIdList):
        totalIndividualStr = ""
        outputFile = open(fileName, "w")
        for index in xrange(len(trafficLightIdList)):
            outputFile.write(trafficLightIdList[index] + ":" + str(individual.genes[index]) + "\n")
            totalIndividualStr = totalIndividualStr + trafficLightIdList[index] + ":" + str(individual.genes[index]);
        outputFile.write("Best Fitness is:" + str(individual.fitness) + "\n")
        outputFile.write(totalIndividualStr)
        outputFile.close()
            
    def startSA(self, maxIterationNum, individualNum, startIndividual):
        bestIndividual = self.iterate(maxIterationNum, startIndividual)
        self.recordBestToFile("best.txt", bestIndividual, Simulate.trafficLightIdList)





















