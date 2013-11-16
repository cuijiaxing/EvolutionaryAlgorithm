import subprocess
import sys
class SUMO:

    @classmethod
    def startSimulator(cls, configFileName):
        pythonCommand = "sumo"
        fh = open("NUL", "w")
        sumoProcess = subprocess.Popen([pythonCommand, "-c", configFileName,"--remote-port", "8813"], stdout = fh,stderr = fh)
        return sumoProcess
