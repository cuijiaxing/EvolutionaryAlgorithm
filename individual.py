import random
from sumo import SUMO
from simulate import Simulate 
from traffic_light import TrafficLight
from info import Info
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
        currentIndex = 0
        for i in xrange(individualNum):
            trafficLightList.append(TrafficLight(inputArray[currentIndex : currentIndex + Info.trafficLightPhaseNumList[i]]));
            currentIndex = currentIndex + Info.trafficLightPhaseNumList[i]
        
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
        for i in xrange(individualNum):
            trafficLightList.append(TrafficLight([cls.getARandomTime() for _  in range(Info.trafficLightPhaseNumList[i])]));
        
        ind = Individual(individualNum)
        ind.genes = trafficLightList
        return ind
    

    #clone the current individual
    def clone(self):
        ind = Individual(self.individualNum)
        ind.genes = []
        ind.MinTime = self.MinTime
        ind.MaxTime = self.MaxTime
        for i in range(len(self.genes)):
            ind.genes.append(TrafficLight(self.genes[i].times))
        return ind
    #get the neighbour of a certain state
    def neighbour(self, strategy, bestInd = None):
        newInstance = self.clone()
        #select one point and change it randomly
        if strategy == "random":
            index = random.randint(0, self.individualNum - 1)
            #change the traffic light into a new one
            newTrac = TrafficLight.getARandomTrafficLight(len(self.genes[index].times), self.MinTime, self.MaxTime)
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
    #deterministic fitness 126                                                           
    #ind = Individual.generateDeterIndividual(4, [40, 30, 15, 50, 35, 30, 20, 20, 20, 80, 18])
    
    ind = Individual.generateDeterIndividual(4, [99,42,11,16,79,83,9,11,89,38,57])
    #ind = Individual.generateRandomIndividual(4)
    #subProcess = SUMO.startSimulator("sumo/SampleRoad/Caltrain/test.sumocfg")
    simulator = Simulate(8813, ind)
    print simulator.beginEvaluate()
    #subProcess.wait()


