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
        if mode not in ['M', 'A']:
            raise ValueError("Modo no válido. Debe ser 'M' o 'A'.")
        self.mode = mode

    def getMode(self):

        return self.mode

    def setPosture(self, args):

        content = args.split("[")[1].split("]")[0]

        partes = content.split()

        x_valor, y_valor, z_valor, e_valor = None, None, None, None

        for parte in partes:
            if parte.startswith("X:"):
                x_valor = float(parte.split(":")[1])
            elif parte.startswith("Y:"):
                y_valor = float(parte.split(":")[1])
            elif parte.startswith("Z:"):
                z_valor = float(parte.split(":")[1])
            elif parte.startswith("E:"):
                e_valor = float(parte.split(":")[1])

        self.x = x_valor
        self.y = y_valor
        self.z = z_valor

    def getPosture(self):

        return [self.x, self.y, self.z]

    def setEffectorStatus(self, status):

        if status not in [True, False]:
            raise Exception("Estado de efector inválido, True o False.")

        self.isEffectorEnabled = status

    def getEffectorStatus(self):

        return self.isEffectorEnabled