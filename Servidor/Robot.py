import math

PI = round(math.pi, 3)


class Robot:

    def __init__(self, name, serial):

        self.serial = serial
        self.name = name
        self.mode = 'M'  # 0 = manual, 1 = automatico
        self.x = None
        self.y = None
        self.z = None
        self.al = None
        self.be = None
        self.ga = None
        self.isEffectorEnabled = False
        self.mappingQuality = 1
        self.goHome()

    def setMode(self, mode):

        self.mode = mode

        if self.mode == 'A':
            self.goHome()
            self.mappingQuality = 2
            self.beginAutomaticMode()

    def getMode(self):

        return self.mode

    def setPosture(self, x, y, z, al, be, ga, s_max=None):

        try:
            x = float(x)
            y = float(y)
            z = float(z)
            al = float(al)
            be = float(be)
            ga = float(ga)
            s_max = float(s_max) if s_max is not None else None

        except Exception as e:

            raise e

        self.x = x
        self.y = y
        self.z = z
        self.al = al
        self.be = be
        self.ga = ga

    def getPosture(self):

        return [self.x, self.y, self.z, self.al, self.be, self.ga]

    def goHome(self):

        try:
            self.serial.writeSerial("G28")
            response = self.serial.readSerial()
            print(response)

        except Exception as e:
            raise e

    def enableEffector(self):

        try:
            self.serial.writeSerial("M3")

        except Exception as e:
            raise e

        self.isEffectorEnabled = True

    def disableEffector(self):

        try:
            self.serial.writeSerial("M5")

        except Exception as e:
            raise e

        self.isEffectorEnabled = False

    def getEffectorStatus(self):

        return self.isEffectorEnabled

    def setMappingQuality(self, quality):

        if quality not in [1, 2, 3]:
            raise Exception("Calidad de mapeo inválida, 1, 2 o 3.")

        self.mappingQuality = quality

    def getMappingQuality(self):

        return self.mappingQuality

    def beginAutomaticMode(self):


        pass