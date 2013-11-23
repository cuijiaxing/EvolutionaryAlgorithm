import random
class TrafficLight:
    ScaleFactor = 1000 #convert between milliseconds and second
    def __init__(self, times):
        self.trafficLightIndexNum = len(times)
        self.times = times
        self.phases = None
    
    #get a random individual
    @classmethod
    def getARandomTrafficLight(cls, num, minValue, maxValue):
        instan = TrafficLight([TrafficLight.scale(random.randint(minValue, maxValue)) for _ in xrange(num)])
        return instan
    
    #reverse the traffic timing by using maxValue - currentValue
    @classmethod
    def getAReverseTrafficLight(cls, ind, minValue, maxValue):
        reverseArray = []
        for i in xrange(len(ind.times)):
            reverseArray.append(cls.scale(maxValue) - ind.times[i])
        return TrafficLight(reverseArray)
    
    #get neighbour with proportion to best fitness
    @classmethod
    def getTrafficLightFromTheBest(cls, bestTrafficLight):
        return TrafficLight(bestTrafficLight.times)
   
    #clone itself
    def clone(self):
        return TrafficLight(self.times)
       
    @classmethod 
    def scale(cls, value):
        return value * cls.ScaleFactor
    
    def __str__(self):
        retStr = ""
        for num in self.times:
            retStr = retStr + str(num / 1000) + ","
        return retStr



