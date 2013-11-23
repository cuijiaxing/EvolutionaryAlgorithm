import os
class Log:
    
    logFileOutputStream = None
    
    @classmethod
    def removeAllLogFile(cls, fileList):
        for fileName in fileList:
            os.remove(fileName)
            
    @classmethod
    def deleteExistingLogFile(cls, fileName = "log.txt"):
        os.remove(fileName)
        
    @classmethod
    def initialize(cls):
        logFileName = "output/acceptance.txt"
        os.remove(logFileName)
        cls.logFileOutputStream = open("output/acceptance.txt", "aw")
        
    
    @classmethod
    def logAcceptanceToFile(cls, iteration, temperature, accepted, logFileName = "output/acceptance.txt"):
        cls.logFileOutputStream.write(str(iteration) + " " + str(temperature) + " " + str(accepted) + "\n")
    
    @classmethod
    def closeAllFile(cls):
        cls.logFileOutputStream.close()
        