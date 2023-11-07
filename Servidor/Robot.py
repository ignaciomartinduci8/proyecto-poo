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
        self.isEffectorEnabled = False

    def setMode(self, mode):

        self.mode = mode

        if self.mode == 'A':
            self.goHome()
            self.beginAutomaticMode()

    def getMode(self):

        return self.mode

    def setPosture(self, x, y, z, s_max=None):

        try:
            x = float(x)
            y = float(y)
            z = float(z)
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

        return [self.x, self.y, self.z]

    def setEffectorStatus(self, status):

        if status not in [True, False]:
            raise Exception("Estado de efector inválido, True o False.")

        self.isEffectorEnabled = status

    def getEffectorStatus(self):

        return self.isEffectorEnabled

    def beginAutomaticMode(self):


        pass