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

        puerto = puerto.upper()

        try:
            self.serial = Serial(puerto, baudrate)
            self.dataLog.logRobotConnection(puerto,baudrate,True)
            self.robot = Robot("Robot POO - Grupo Negro", self.serial)
            self.isConnected = True

            res = []

            for i in range(2):
                res.append(self.serial.readSerial())
                time.sleep(0.3)

            self.serial.writeSerial("M114")

            for i in range(2):
                res.append(self.serial.readSerial())
                time.sleep(0.3)

            self.robot.setPosture(res[3])
            self.dataLog.logRobotStatus(self.robot.getMode(),self.robot.getPosture()[0],self.robot.getPosture()[1],self.robot.getPosture()[2],self.robot.getEffectorStatus())
            return res

        except Exception as e:

            self.serial = None
            self.robot = None
            raise e

    def disconnect(self):

        try:

            if self.serial is not None:
                self.dataLog.logRobotConnection(self.serial.getData()[0],self.serial.getData()[1],False)
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
                    self.dataLog.logHome(self.robot.getPosture()[0],self.robot.getPosture()[1],self.robot.getPosture()[2])
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
                self.dataLog.logRobotMove(self.robot.getPosture()[0],self.robot.getPosture()[1],self.robot.getPosture()[2])
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
                self.dataLog.logRobotEffector(True)
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

        if not self.robot.getEffectorStatus():

            raise Exception('Ya se ha desactivado el effector.')

        try:
            self.serial.writeSerial("M5")

            res = self.serial.readSerial()

            if "INFO" in res:
                self.robot.setEffectorStatus(False)
                self.dataLog.logRobotEffector(False)
                return res
            else:
                raise Exception(res)

        except Exception as e:
            raise e

    def getRobotStatus(self):

        if not self.isConnected:

            raise Exception("No se ha conectado un robot.")

        x, y, z = self.robot.getPosture()

        self.dataLog.logRobotStatus(self.robot.getMode(),x,y,z,self.robot.getEffectorStatus())

        return [self.robot.getMode(), self.robot.getPosture(), self.robot.getEffectorStatus()]

    def report(self):

        res = ["Reporte de estado de robot y de logs."]

        if self.isConnected:
            res.append("Robot conectado")
            res.append(f"Modo de robot: {self.robot.getMode()}")
            res.append(f"Posición actual: {self.robot.getPosture()} mm")
            res.append(f"Estado del efector: {self.robot.getEffectorStatus()}")

        else:
            res.append("Robot desconectado")

        logData = self.dataLog.getLastSession()

        if logData is not None:

            res.append(f"La última sesión comenzó a las: {logData[0]}")
            logData.pop(0)
            res.append("Log de la última sesión:")

            for line in logData:
                res.append(line)

        else:

            res.append("No hay logs de sesión.")

        return res