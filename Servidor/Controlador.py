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

            else:
                raise Exception("No hay robot conectado")

        except Exception as e:

            raise e

# Métodos de robot

    def goHome(self):

        if not self.isConnected:
            raise Exception("No hay robot conectado")

        if self.robot.getMode() != 'M':
            raise Exception("Robot en modo automático")

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

                    self.robot.setPosture(res[3])

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
    
    def learnPath(self, path_filename):
        with open(path_filename, 'w') as file:
            for command in self.path:
                file.write(command + '\n')

    def loadAutomaticFile(self):
        filename = input("Introduce el nombre del archivo automático: ")
        try:
            with open(filename, 'r') as file:
                self.automatic_file = file.readlines()
        except FileNotFoundError:
            print("Archivo no encontrado.")
            self.mode = 'manual'

    def executeAutomaticMode(self):
        if self.automatic_file:
            for line in self.automatic_file:
                pass
        else:
            print("No hay archivo automático cargado.")


    def moveEffector(self, x, y, z, s_max=0):

        if not self.isConnected:
            raise Exception("Error - No se ha conectado un robot.")

        if self.robot.getMode() != 'M':
            raise Exception('Operación no válida, robot en modo automático')

        try:

            self.serial.writeSerial(f"G0X{x}Y{y}Z{z}F{s_max}")

            res = self.serial.readSerial()

            if "ERROR" not in res:
                self.robot.setPosture(res)
                return res

            else:
                raise Exception(res)

        except Exception as e:

            raise e

    def enableEffector(self):

        if not self.isConnected:
            raise Exception("No se ha conectado un robot.")

        if self.robot.getMode() != 'M':
            raise Exception('Operación no válida, robot en modo automático.')

        if self.robot.getEffectorStatus():
            raise Exception('Ya se ha activado el effector.')

        try:
            self.serial.writeSerial("M3")

            res = self.serial.readSerial()

            if "INFO" in res:
                self.robot.setEffectorStatus(True)
                return res
            else:
                raise Exception(res)

        except Exception as e:
            raise e

    def disableEffector(self):

        if not self.isConnected:

            raise Exception("No se ha conectado un robot.")

        if self.robot.getMode() != 'M':
            raise Exception('Operación no válida, robot en modo automático')

        if not self.robot.enableEffector():

            raise Exception('Ya se ha desactivado el effector.')

        try:
            self.serial.writeSerial("M5")

            res = self.serial.readSerial()

            if "INFO" in res:
                self.robot.setEffectorStatus(False)
                return res
            else:
                raise Exception(res)

        except Exception as e:
            raise e

    def getEffectorStatus(self):

        if not self.isConnected:
            raise Exception("No se ha conectado un robot.")

        self.robot.getEffectorStatus()

    def getPosture(self):

        if not self.isConnected:
            raise Exception("No se ha conectado un robot.")

        return self.robot.getPosture()
