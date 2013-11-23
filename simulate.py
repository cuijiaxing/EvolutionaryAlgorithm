import traci

class Simulate:
    trafficLightIdList = ["65470359", "65535917", "65531994", "65620946"]
    trafficLightPhaseNumList = [4, 2, 3, 2]
    
    
    def __init__(self, portNum, individual):
        """
        @param portNum the port that this class can use to evaluate the individuals, also the port num is used to identify a connection to the sumo server
        @param genes the traffic timeing for each traffic light
        """
        
        self.portNum = portNum
        #timing for each traffic light
        self.individual = individual 
    
    #using strategy design pattern to get fitness
    def beginEvaluate(self, strategyStr = "arrivedNumOnly"):
        if strategyStr == "arrivedNumOnly" :
            return self.evaluateArrivedNumMinusTeleportNum()
        elif strategyStr == "arrivedNumMinusWaitingTime":
                return self.evaluateArrivedNumMinusWaitingTime(1, 1)
            
    def evaluateArrivedNumMinusTeleportNum(self):
        """
        Given the parameters during initialization, we run the simulator to get the fitness
        using port num to identify a connection
        """
        traci.init(self.portNum, 10, "localhost", str(self.portNum))
        #traverse all the traffic lights
        for i in xrange(len(self.trafficLightIdList)):
            #traverse all the traffic lights
            tlsLogicList = traci.trafficlights.getCompleteRedYellowGreenDefinition(self.trafficLightIdList[i])
            #One traffic light has only one phase list now
            tlsLogicList = tlsLogicList[0]
            #each traffic light has several phases
            phaseList = []
            #traverse all the phase
            for j in xrange(len(tlsLogicList._phases)):
#                 print self.individual.genes[i].times[j]
                phaseList.append(traci.trafficlights.Phase(self.individual.genes[i].times[j], self.individual.genes[i].times[j], self.individual.genes[i].times[j], tlsLogicList._phases[j]._phaseDef))
            tlsLogicList._phases = phaseList
            traci.trafficlights.setCompleteRedYellowGreenDefinition(self.trafficLightIdList[i], tlsLogicList)

        totalNumPassed = 0
        for _ in xrange(1000):
            traci.simulationStep()
            totalNumPassed = totalNumPassed + traci.simulation.getArrivedNumber() - traci.simulation.getEndingTeleportNumber()
        traci.close()
        self.fitness = totalNumPassed
        return totalNumPassed
    
    def evaluateArrivedNumMinusWaitingTime(self, coefficientArrivedNum = 1, coefficientWaitingTime = 1):
        """
        Given the parameters during initialization, we run the simulator to get the fitness
        using port num to identify a connection
        """
        traci.init(self.portNum, 10, "localhost", str(self.portNum))
        #traverse all the traffic lights
        for i in xrange(len(self.trafficLightIdList)):
            #traverse all the traffic lights
            tlsLogicList = traci.trafficlights.getCompleteRedYellowGreenDefinition(self.trafficLightIdList[i])
            #One traffic light has only one phase list now
            tlsLogicList = tlsLogicList[0]
            #each traffic light has several phases
            phaseList = []
            #traverse all the phase
            for j in xrange(len(tlsLogicList._phases)):
#                 print self.individual.genes[i].times[j]
                phaseList.append(traci.trafficlights.Phase(self.individual.genes[i].times[j], self.individual.genes[i].times[j], self.individual.genes[i].times[j], tlsLogicList._phases[j]._phaseDef))
            tlsLogicList._phases = phaseList
            traci.trafficlights.setCompleteRedYellowGreenDefinition(self.trafficLightIdList[i], tlsLogicList)

        totalNumPassed = 0
        totalWaitingNum  = 0;
        for _ in xrange(700):
            traci.simulationStep()
            totalNumPassed = totalNumPassed + traci.simulation.getArrivedNumber() - traci.simulation.getEndingTeleportNumber()
            #totalWaitingNum = totalWaitingNum + traci.multientryexit.getLastStepHaltingNumber("e3_1")
        traci.close()
        self.fitness = coefficientArrivedNum * totalNumPassed - coefficientWaitingTime * totalWaitingNum
        return self.fitness 



