import random
class TrafficLight:
    scale = 1000 #convert between milliseconds and second
    def __init__(self, times):
        self.trafficLightIndexNum = len(times)
        self.times = times

    @classmethod
    def getARandomTrafficLight(cls, num, minValue, maxValue):
        instan = TrafficLight([random.randint(minValue, maxValue) * cls.scale for _ in xrange(num)])
        return instan

    def __str__(self):
        retStr = ""
        for num in self.times:
            retStr = retStr + str(num / 1000) + " "
        return retStr



