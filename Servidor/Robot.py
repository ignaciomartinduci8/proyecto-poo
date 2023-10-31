

class Robot:

    def __init__(self):

        self.mode = 0 # 0 = manual, 1 = automatico

    def setMode(self, mode):

        self.mode = mode

    def getMode(self):

        return self.mode