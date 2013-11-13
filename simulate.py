import traci

class Simulate:
    trafficLightIdList = None
    
    def __init__(self, portNum, individual):
        """
        @param portNum the port that this class can use to evaluate the individuals, also the port num is used to identify a connection to the sumo server
        @param genes the traffic timeing for each traffic light
        """
        
        self.portNum = portNum
        #timing for each traffic light
        self.individual = individual 

    def beginEvaluate(self):
        """
        Given the parameters during initialization, we run the simulator to get the fitness
        using port num to identify a connection
        """
        traci.init(self.portNum, 10, "localhost", str(self.portNum))
        #print(traci.simulation.getCurrentTime())
        #get all the traffic lights id in the network
        self.trafficLightIdList = traci.trafficlights.getIDList()
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
        if Simulate.trafficLightIdList == None:
            Simulate.trafficLightIdList = traci.trafficlights.getIDList()

        inductionLoopIdList = traci.inductionloop.getIDList()
        totalSpeed = 0
        for _ in xrange(1000):
            traci.simulationStep()
            #get the speed from all detectors
            #notice that the value CA_CERTS
#             if traci.inductionloop.getLastStepMeanSpeed(inductionLoopIdList[0]) > 1:
#                 totalSpeed = totalSpeed + traci.inductionloop.getLastStepMeanSpeed(inductionLoopIdList[0])
            for inductionLoop in inductionLoopIdList:
                if traci.inductionloop.getLastStepMeanSpeed(inductionLoop) > 1:
                    totalSpeed = totalSpeed + traci.inductionloop.getLastStepMeanSpeed(inductionLoop)
                    #totalSpeed = totalSpeed + traci.inductionloop.getLastStepVehicleNumber(inductionLoop)
        
        traci.close()
        self.fitness = totalSpeed / len(inductionLoopIdList)
        return totalSpeed / len(inductionLoopIdList)



