import random
from sumo import SUMO
from simulate import Simulate 
from traffic_light import TrafficLight
class Individual:
    
    scale = TrafficLight.ScaleFactor
    MaxTime = 100 
    MinTime =  0 
    NumForEachTrafficLight = 4

    def __init__(self, individualNum):
        self.individualNum = individualNum
        self.fitness = 0
    
    #generate a deterministic timing
    @classmethod
    def generateDeterIndividual(cls, individualNum, inputArray):
        #scale the inputArray
        for i in xrange(len(inputArray)):
            inputArray[i] = inputArray[i] * cls.scale
        trafficLightList = []
        for i in xrange(individualNum):
            trafficLightList.append(TrafficLight(inputArray[i * cls.NumForEachTrafficLight : (i + 1) * cls.NumForEachTrafficLight]));
        
        ind = Individual(individualNum)
        ind.genes = trafficLightList
        return ind
        
    @classmethod
    def getARandomTime(cls):
        return random.randint(cls.MinTime, cls.MaxTime) * cls.scale 
    #generate random traffic timing
    @classmethod
    def generateRandomIndividual(cls, individualNum):
        trafficLightList = []
        for _ in xrange(individualNum):
            trafficLightList.append(TrafficLight([cls.getARandomTime() for _ in range(cls.NumForEachTrafficLight)]));
        
        ind = Individual(individualNum)
        ind.genes = trafficLightList
        return ind
    

    #clone the current individual
    def clone(self):
        ind = Individual(self.individualNum)
        ind.genes = self.genes
        return ind
    #get the neighbour of a certain state
    def neighbour(self, strategy, bestInd = None):
        newInstance = self.clone()
        #select one point and change it randomly
        if strategy == "random":
            index = random.randint(0, self.individualNum - 1)
            #change the traffic light into a new one
            newTrac = TrafficLight.getARandomTrafficLight(self.NumForEachTrafficLight, self.MinTime, self.MaxTime)
        elif strategy == "reverse":
            index = random.randint(0, self.individualNum - 1)
            newTrac = TrafficLight.getAReverseTrafficLight(newInstance.genes[index], self.MinTime, self.MaxTime)
        elif strategy == "extractBest":
            index = random.randint(0, self.individualNum - 1)
            if bestInd is None:
                newTrac = TrafficLight.getARandomTrafficLight(self.NumForEachTrafficLight, self.MinTime, self.MaxTime)
            else:
                newTrac = TrafficLight.getTrafficLightFromTheBest(bestInd.genes[index])
            
        newInstance.genes[index] = newTrac
        return newInstance

    #evaluate the fitness
    def evaluate(self, dataDir):
        subProcess = SUMO.startSimulator(dataDir + "test.sumocfg")
        ind = Simulate(8813, self)
        self.fitness = ind.beginEvaluate()
        subProcess.wait()

if __name__ == "__main__":
    #deterministic fitness 431.102042914                                                               
    ind = Individual.generateDeterIndividual(4, [21,67,36,16,82,65,88,32,31,1,35,30,97,71,66,85])
    #ind = Individual.generateRandomIndividual(4)
    simulator = Simulate(8813, ind)
    print simulator.beginEvaluate()

