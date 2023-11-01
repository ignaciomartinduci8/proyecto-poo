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

        if self.mode == 'A':
            self.goHome()
            self.mappingQuality = 2

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

        except  Exception as e:

            raise e

        conditions = [

                x >= 0 and x <= 600,
                y >= -300 and y <= 300,
                z >= 0 and z <= 600,
                al >= 0 and al <= 2*PI,
                be >= -PI/2 and be <= PI/2,
                ga >= -PI/2 and ga <= PI/2

        ]

        if not all(conditions):

            raise Exception("Error - argumentos inválidos, verifica valores, espacios de trabajo, y tipos de datos.")

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

