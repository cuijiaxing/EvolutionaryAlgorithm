from simulate import Simulate
import math
import random
from log import Log

class SA:
    
    dataDir = "."
    temperatureScale = 100.0 #scale the temperature into the interval[0,100]
    MaxFitness = 200
    NormalizeFactor = 30 
    maxIterationNum = 200 #best fitness = -2278 
    trafficLightNum = 4
    totalTimeScale = NormalizeFactor 
    
    def __init__(self, maxIterNum, trafficLightNum):
        self.maxIterationNum = maxIterNum
        self.trafficLightNum = trafficLightNum
        

    def temperature(self, currentTime, totalTime):
        
        temp = (totalTime - currentTime) * 1.0  / totalTime
        if temp == 0:
            temp = 0.00001
        return temp * self.totalTimeScale
    
    def P(self, prevIndividual, individual, time):
        
        #always accept better ones
        if individual.fitness > prevIndividual.fitness:
            return 1.0
        else:
            deltaFit = (prevIndividual.fitness - individual.fitness) * 1.0 / self.MaxFitness
            return 1 / (1 + math.exp((deltaFit) * self.NormalizeFactor/ ((time + 1.0) )))
            #deltaT = (time) * 1.0 / self.totalTimeScale
            #return math.exp(-1 *  deltaFit / deltaT) / 2
            #return math.exp((-1.0 * delta)  / (time + 1)
    
    @classmethod
    def oneOverXFormProb(cls, prevIndividual, individual, time):
        #always accept better ones
        if individual.fitness > prevIndividual.fitness:
            return 1.0
        else:
            delta = prevIndividual.fitness - individual.fitness
            currentMaxProb = 1 - 1 / ((time + 1)**(1 / 10.0))
            return currentMaxProb * (1 - delta * 1.0 / individual.fitness) #scale it
            #return math.exp((-1.0 * delta)  / (time + 1)
        
        


    def iterate(self, maxIterationNum, startIndividual):
        #define best individual and best energy
        bestIndividual = None;
        #define current individual and current energy
        bestEnergy = currentEnergy = -9999999999 
        currentIndividual = None
        timeCount = 1 #it has to be at 1 because in temperature function ,it is a denomerator 
        #define the optimal fitness the system can achieve
        optimalEnergy = 99999999 
        
        #before start, evaluate the start individual first
        startIndividual.evaluate(self.dataDir) #get the fitness
        currentIndividual = startIndividual
        currentEnergy = currentIndividual.fitness
        #record fitness
        fitnessOutputFile = open("output/fitness" + str(maxIterationNum) + ".txt", "w")
        #prepare log file
        Log.initialize()
        while timeCount < maxIterationNum and currentEnergy < optimalEnergy:
            #get the current temperature
            T = self.temperature(timeCount, maxIterationNum)
            #get the neighbour
            newInd = currentIndividual.neighbour("random", bestIndividual)
            newInd.evaluate(self.dataDir)
            print newInd.fitness
            
            acquiredP = self.P(currentIndividual, newInd, T)
            #acquiredP = self.oneOverXFormProb(currentIndividual, newInd, T)
            criterionP = random.random()
            print(acquiredP)
            if acquiredP > criterionP:
                if newInd.fitness < currentIndividual.fitness:
                    Log.logAcceptanceToFile(timeCount, T, 1)
                else:
                    Log.logAcceptanceToFile(timeCount, T, 0)
                currentIndividual = newInd
                currentEnergy = newInd.fitness
            else:
                Log.logAcceptanceToFile(timeCount, T, 0)
                
            if newInd.fitness > bestEnergy:
                bestIndividual = newInd
                bestEnergy = newInd.fitness
            timeCount = timeCount + 1
            fitnessOutputFile.write(str(currentIndividual.fitness) + "\n")
        fitnessOutputFile.close()
            
            
        #close log file
        Log.closeAllFile()
        return bestIndividual
    
    def recordBestToFile(self, fileName, individual, trafficLightIdList):
        totalIndividualStr = ""
        outputFile = open(fileName, "w")
        for index in xrange(len(trafficLightIdList)):
            outputFile.write(trafficLightIdList[index] + ":" + str(individual.genes[index]) + "\n")
            totalIndividualStr = totalIndividualStr + str(individual.genes[index]) ;
        outputFile.write("Best Fitness is:" + str(individual.fitness) + "\n")
        outputFile.write(totalIndividualStr)
        outputFile.close()
            
    def startSA(self, dataDir, startIndividual):
        self.dataDir = dataDir
        bestIndividual = self.iterate(self.maxIterationNum, startIndividual)
        self.recordBestToFile("output/best" + str(self.maxIterationNum) + ".txt", bestIndividual, Simulate.trafficLightIdList)
