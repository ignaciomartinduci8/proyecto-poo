import time
from threading import Thread
import os

from Serial import Serial
from Robot import Robot


class Controlador:

    def __init__(self, dataLog):
        self.isConnected = False
        self.serial = None
        self.robot = None
        self.dataLog = dataLog
        self.automatic_file = None
        self.auto_thread = None
        self.isLearning = False
        if not os.path.exists("./Autos"):
            os.makedirs("./Autos")
        
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
    def setRobotMode(self, mode, args=None):

        if not self.isConnected:

            raise Exception("No se ha conectado un robot.")
        try:

            if mode == 'A':

                if args not in self.listAutomaticFiles():
                    self.automatic_file = None
                    raise Exception("Archivo no encontrado.")

                self.robot.setMode('A')
                self.automatic_file = args
                self.automaticMode()

            elif mode == 'M':

                self.robot.setMode('M')
                return self.manualMode()

        except Exception as e:

            raise e

    def manualMode(self):
        try:
            if self.auto_thread and self.auto_thread.is_alive():
                self.auto_thread.join(timeout=2)
                self.automatic_file = None
                self.auto_thread = None
                self.dataLog.logRobotMode(False)

                res = self.goHome()

                res.append("Modo automático detenido.")

                self.robot.setPosture(res[3])

                return res

        except Exception as e:
            raise e

    def listAutomaticFiles(self):

        return os.listdir("./Autos")

    def automaticMode(self):

        try:

            self.auto_thread = Thread(target=self.runAutomaticFile)
            self.auto_thread.start()

        except Exception as e:
            raise e

    def runAutomaticFile(self):

        try:

            self.dataLog.logRobotMode(True)

            while True:

                with open(f"./Autos/{self.automatic_file}", "r") as f:

                    for line in f.readlines():

                        self.serial.writeSerial(line)
                        time.sleep(.3)

                        for i in range(4):
                            self.serial.flushInput()
                            time.sleep(.5)

                        self.dataLog.logAutomatic(line)

                    if self.auto_thread is None:

                        return "Modo automático detenido."

        except Exception as e:
            raise e

    def learnAutomaticFile(self, gcode):

        with open(f"./Autos/{self.automatic_file}", "a") as f:
            f.write(gcode)
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def toggleLearn(self):

        self.isLearning = not self.isLearning

        if self.isLearning:
            return "Modo aprendizaje activado."
        else:
            return "Modo aprendizaje desactivado."

    def moveEffector(self, x, y, z, s_max=0):

        if not self.isConnected:
            raise Exception("Error - No se ha conectado un robot.")

        if self.robot.getMode() != 'M':
            raise Exception('Operación no válida, robot en modo automático')

        try:

            inst = f"G0X{x}Y{y}Z{z}F{s_max}"
            self.serial.writeSerial(inst)

            res = self.serial.readSerial()

            if "ERROR" not in res:
                self.robot.setPosture(res)
                self.dataLog.logRobotMove(self.robot.getPosture()[0],self.robot.getPosture()[1],self.robot.getPosture()[2])

                if self.isLearning:

                    self.learnAutomaticFile(inst)

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
                self.learnAutomaticFile("M3")
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
            res.append(f"Log de la última sesión ({len(logData)}):")

            for line in logData:
                res.append(line)

        else:

            res.append("No hay logs de sesión.")

        return res