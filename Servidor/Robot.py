import math

PI = round(math.pi, 3)


class Robot:

    def __init__(self, name):

        self.name = name
        self.mode = 'M'  # 0 = manual, 1 = automatico
        self.x = None
        self.y = None
        self.z = None
        self.al = None
        self.be = None
        self.ga = None
        self.goHome()
        self.isEffectorEnabled = False
        self.mappingQuality = 1

    def setMode(self, mode):

        self.mode = mode

    def getMode(self):

        return self.mode

    def setPosture(self, x, y, z, al, be, ga, s_max=None):

        self.x = x
        self.y = y
        self.z = z
        self.al = al
        self.be = be
        self.ga = ga

    def getPosture(self):

        return [self.x, self.y, self.z, self.al, self.be, self.ga]

    def goHome(self):

        self.x = 300
        self.y = 0
        self.z = 250
        self.al = PI
        self.be = 0
        self.ga = 0


    def enableEffector(self):

        self.isEffectorEnabled = True

    def disableEffector(self):

        self.isEffectorEnabled = False

    def getEffectorStatus(self):

        return self.isEffectorEnabled

    def setMappingQuality(self, quality):

        if quality not in [1, 2, 3]:
            raise Exception("Calidad de mapeo inválida, 1, 2 o 3.")

        self.mappingQuality = quality

    def getMappingQuality(self):

        return self.mappingQuality

