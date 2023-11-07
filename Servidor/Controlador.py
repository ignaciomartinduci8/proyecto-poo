import time

from Serial import Serial
from Robot import Robot


class Controlador:

    def __init__(self, dataLog):
        self.isConnected = False
        self.serial = None
        self.robot = None
        self.dataLog = dataLog

# Métodos de conexión y desconexión

    def connect(self, puerto, baudrate):

        try:
            self.serial = Serial(puerto, baudrate)
            self.robot = Robot("Robot POO - Grupo Negro", self.serial)
            self.isConnected = True

            res = []

            for i in range(2):

                res.append(self.serial.readSerial())
                time.sleep(0.3)

            return res


        except Exception as e:

            self.serial = None
            self.robot = None
            raise e

    def disconnect(self):

        try:

            if self.serial is not None:
                del self.serial
                self.isConnected = False
                return "Robot en puerto serie desconectado"

        except Exception as e:

            raise e

    def getIsConnected(self):

        return self.isConnected

# Métodos de robot

    def goHome(self):

        try:
            self.serial.writeSerial("G28")

            res = []

            for i in range(2):

                res.append(self.serial.readSerial())
                time.sleep(.3)

            if "ERROR" not in res:

                self.serial.writeSerial("M114")

                for i in range(2):

                    res.append(self.serial.readSerial())
                    time.sleep(.3)

                if "ERROR" not in res:

                    return res

                else:

                    raise Exception(res)

            else:
                raise Exception(res)

        except Exception as e:

            raise e

    def setRobotMode(self, mode):

        if not self.isConnected:

            raise Exception("No se ha conectado un robot.")

        try:

            self.robot.setMode(mode)

        except Exception as e:

            raise e

    def moveEffector(self, x, y, z, s_max=None):

        if self.robot.getMode() != 'M':
            raise Exception('Operación no válida, robot en modo automático')

        if not self.isConnected:

            raise Exception("Error - No se ha conectado un robot.")

        try:

            self.robot.setPosture(x, y, z, s_max)

        except Exception as e:

            raise e

    def enableEffector(self):

        if self.robot.getMode() != 'M':
            raise Exception('Operación no válida, robot en modo automático.')

        if not self.isConnected:
            raise Exception("No se ha conectado un robot.")

        if self.robot.getEffectorStatus():
            raise Exception('Ya se ha activado el effector.')

        try:
            self.serial.writeSerial("G3")

            res = self.serial.readSerial()

            if "INFO" in res:
                return res
            else:
                raise Exception(res)

        except Exception as e:
            raise e

    def disableEffector(self):

        if self.robot.getMode() != 'M':
            raise Exception('Operación no válida, robot en modo automático')

        if not self.isConnected:

            raise Exception("No se ha conectado un robot.")

        if not self.robot.enableEffector():

            raise Exception('Ya se ha desactivado el effector.')

        try:

            self.robot.disableEffector()

        except Exception as e:
            raise e

    def getEffectorStatus(self):


        if not self.isConnected:
            raise Exception("No se ha conectado un robot.")

        self.robot.getEffectorStatus()

    def getPosture(self):

        return self.robot.getPosture()


    def setMappingQuality(self, quality):

        if not self.isConnected:
            raise Exception("No se ha conectado un robot.")

        try:

            self.robot.setMappingQuality(quality)

        except Exception as e:

            raise e

