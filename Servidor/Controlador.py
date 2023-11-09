import time
from threading import Thread
import os
import shutil
import json

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
        self.backupDir = './Backups'
        self.usersPath = './Users/registered_users.json'
        self.workingID = None
        
# Métodos de conexión y desconexión

    def connect(self, puerto, baudrate, ID=None):

        RPCprocess = False

        if self.workingID is not None and self.workingID != ID:

            raise Exception("Otro cliente está conectando el robot.")

        elif self.workingID is None and ID is not None:

            self.workingID = ID
            RPCprocess = True

        elif self.workingID is not None and self.workingID == ID:

            RPCprocess = True


        puerto = puerto.upper()

        try:
            self.serial = Serial(puerto, baudrate)
            self.dataLog.logRobotConnection(puerto,baudrate,True,RPCprocess)
            self.robot = Robot("Robot POO - Grupo Negro", self.serial, 100, 300, 200, 1, 3000)
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
            self.dataLog.logRobotStatus(self.robot.getMode(),self.robot.getPosture()[0],self.robot.getPosture()[1],self.robot.getPosture()[2],self.robot.getEffectorStatus(),RPCprocess)
            return res

        except Exception as e:

            self.serial = None
            self.robot = None
            raise e

    def disconnect(self, ID=None):

        RPCprocess = False

        if self.workingID is not None and self.workingID != ID:
            raise Exception("Otro cliente está conectado al robot.")

        elif self.workingID is not None and self.workingID == ID:
            RPCprocess = True


        try:

            if self.serial is not None:
                self.dataLog.logRobotConnection(self.serial.getData()[0],self.serial.getData()[1],False,RPCprocess)
                del self.serial
                self.isConnected = False
                self.workingID = None
                return "Robot en puerto serie desconectado"

            else:
                raise Exception("No hay robot conectado")

        except Exception as e:

            raise e

# Métodos de robot
    def setRobotMode(self, mode, filename=None, ID=None):

        RPCprocess = False

        if self.workingID is not None and self.workingID != ID:
            raise Exception("Otro cliente está conectado al robot.")

        elif self.workingID is not None and self.workingID == ID:
            RPCprocess = True

        if not self.isConnected:

            raise Exception("No se ha conectado un robot.")
        try:

            if mode == 'A':

                if not os.path.exists("./Autos"):
                    os.makedirs("./Autos")

                if filename not in self.listAutomaticFiles():
                    self.automatic_file = None
                    raise Exception("Archivo no encontrado.")

                self.robot.setMode('A')
                self.automatic_file = filename
                self.automaticMode(RPCprocess)

            elif mode == 'M':

                self.robot.setMode('M')
                return self.manualMode(RPCprocess)

        except Exception as e:

            raise e

    def manualMode(self,RPCProcess=False):
        try:
            if self.auto_thread and self.auto_thread.is_alive():
                self.auto_thread.join(timeout=2)
                self.automatic_file = None
                self.auto_thread = None
                self.dataLog.logRobotMode(False,RPCProcess)

                res = self.goHome()

                res.append("Modo automático detenido.")

                self.robot.setPosture(res[3])

                return res

        except Exception as e:
            raise e

    def listAutomaticFiles(self):

        return os.listdir("./Autos")

    def automaticMode(self,RPCProcess=False):

        try:

            self.auto_thread = Thread(target=self.runAutomaticFile(RPCProcess))
            self.auto_thread.start()

        except Exception as e:
            raise e

    def runAutomaticFile(self,RPCProcess=False):

        try:

            self.dataLog.logRobotMode(True,RPCProcess)

            while True:

                with open(f"./Autos/{self.automatic_file}", "r") as f:

                    for line in f.readlines():

                        if "GCODE" in line:
                            continue

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

        with open(f"./Autos/{self.automatic_file}", 'a') as f:
            f.write(gcode+'\n')
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def toggleLearn(self,onOff,filename=None, ID=None):

        RPCprocess = False

        if self.workingID is not None and self.workingID != ID:
            raise Exception("Otro cliente está conectado al robot.")

        elif self.workingID is not None and self.workingID == ID:
            RPCprocess = True

        if not self.isConnected:
            raise Exception("No se ha conectado un robot.")

        try:
            if onOff == 'S' and not self.isLearning:
                self.isLearning = True

                self.automatic_file = filename
                self.dataLog.logToggleLearn(True,RPCprocess)

                with open(f"./Autos/{self.automatic_file}", "w") as f:
                    f.write("================== GCODE AUTOMATICO ==================\n")
                    f.flush()
                    os.fsync(f.fileno())
                    f.close()

                return "Modo aprendizaje activado."

            elif onOff == 'S' and self.isLearning:
                raise Exception ("Modo aprendizaje ya activado")                
    
            elif onOff == 'N' and self.isLearning:
                self.isLearning = False
                self.dataLog.logToggleLearn(False,RPCprocess)
                return "Modo aprendizaje desactivado."

            elif onOff == 'N' and not self.isLearning:
                raise Exception ("Modo aprendizaje ya desactivado")
            
            else:
                raise Exception("Opción no válida")
            
        except Exception as e:
            raise e

    def moveEffector(self, x, y, z, s_max=0, ID=None):

        RPCprocess = False

        if self.workingID is not None and self.workingID != ID:
            raise Exception("Otro cliente está conectado al robot.")

        elif self.workingID is not None and self.workingID == ID:
            RPCprocess = True

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
                self.dataLog.logRobotMove(self.robot.getPosture()[0],self.robot.getPosture()[1],self.robot.getPosture()[2],RPCprocess)


                if self.isLearning:

                    self.learnAutomaticFile(inst)

                return res

            else:
                raise Exception(res)

        except Exception as e:

            raise e

    def enableEffector(self, ID=None):

        RPCprocess = False

        if self.workingID is not None and self.workingID != ID:
            raise Exception("Otro cliente está conectado al robot.")

        elif self.workingID is not None and self.workingID == ID:
            RPCprocess = True

        if not self.isConnected:
            raise Exception("No se ha conectado un robot.")

        if self.robot.getMode() != 'M':
            raise Exception('Operación no válida, robot en modo automático.')

        if self.robot.getEffectorStatus():
            raise Exception('Ya se ha activado el effector.')

        try:
            
            self.serial.writeSerial("M3")
            res = self.serial.readSerial()
            inst="M3"

            if "INFO" in res:
                self.robot.setEffectorStatus(True)
                self.dataLog.logRobotEffector(True,RPCprocess)
                self.learnAutomaticFile("M3")

                if self.isLearning:
                    
                    self.learnAutomaticFile(inst)

                return res
            else:
                raise Exception(res)

        except Exception as e:
            raise e

    def disableEffector(self, ID=None):

        RPCprocess = False

        if self.workingID is not None and self.workingID != ID:
            raise Exception("Otro cliente está conectado al robot.")

        elif self.workingID is not None and self.workingID == ID:
            RPCprocess = True

        if not self.isConnected:

            raise Exception("No se ha conectado un robot.")

        if self.robot.getMode() != 'M':
            raise Exception('Operación no válida, robot en modo automático')

        if not self.robot.getEffectorStatus():

            raise Exception('Ya se ha desactivado el effector.')

        try:
            self.serial.writeSerial("M5")
            inst="M5"
            res = self.serial.readSerial()

            if "INFO" in res:
                self.robot.setEffectorStatus(False)
                self.dataLog.logRobotEffector(False,RPCprocess)
                if self.isLearning:
                    
                    self.learnAutomaticFile(inst)
                return res
            else:
                raise Exception(res)

        except Exception as e:
            raise e

    def enableMotors(self, ID=None):

        RPCprocess = False

        if self.workingID is not None and self.workingID != ID:
            raise Exception("Otro cliente está conectado al robot.")

        elif self.workingID is not None and self.workingID == ID:
            RPCprocess = True

        if not self.isConnected:

            raise Exception("No se ha conectado un robot.")

        if self.robot.getMode() != 'M':

            raise Exception('Operación no válida, robot en modo automático')

        if self.robot.getMotorsStatus():

            raise Exception('Ya se han activado los motores.')

        try:

            self.serial.writeSerial("M17")
            res = self.serial.readSerial()

            if "INFO" in res:

                self.robot.setMotors(True)
                self.dataLog.logMotors(True,RPCprocess)
                return res

            else:

                raise Exception(res)

        except Exception as e:

            raise e

    def disableMotors(self, ID=None):

        RPCprocess = False

        if self.workingID is not None and self.workingID != ID:
            raise Exception("Otro cliente está conectado al robot.")

        elif self.workingID is not None and self.workingID == ID:
            RPCprocess = True

        if not self.isConnected:

            raise Exception("No se ha conectado un robot.")

        if self.robot.getMode() != 'M':

            raise Exception('Operación no válida, robot en modo automático')

        if not self.robot.getMotorsStatus():

            raise Exception('Ya se han desactivado los motores.')

        try:

            self.serial.writeSerial("M18")
            res = self.serial.readSerial()

            if "INFO" in res:

                self.robot.setMotors(False)
                self.dataLog.logMotors(False,RPCprocess)
                return res

            else:

                raise Exception(res)

        except Exception as e:

            raise e

    def goHome(self, ID=None):

        RPCprocess = False

        if self.workingID is not None and self.workingID != ID:
            raise Exception("Otro cliente está conectado al robot.")

        elif self.workingID is not None and self.workingID == ID:
            RPCprocess = True

        if not self.isConnected:
            raise Exception("No hay robot conectado")

        if self.robot.getMode() != 'M':
            raise Exception("Robot en modo automático")

        try:
            self.serial.writeSerial("G28")
            inst="G28"
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
                    self.dataLog.logHome(self.robot.getPosture()[0],self.robot.getPosture()[1],self.robot.getPosture()[2],RPCprocess)

                    if self.isLearning:
                        self.learnAutomaticFile(inst)
                    return res

                else:

                    raise Exception(res)

            else:
                raise Exception(res)

        except Exception as e:

            raise e

    def getRobotStatus(self):

        RPCprocess = False

        if self.workingID is not None:
            RPCprocess = True

        if not self.isConnected:

            raise Exception("No se ha conectado un robot.")

        x, y, z = self.robot.getPosture()

        self.dataLog.logRobotStatus(self.robot.getMode(),x,y,z,self.robot.getEffectorStatus(),RPCprocess)

        return [self.robot.getMode(), self.robot.getPosture(), self.robot.getEffectorStatus(), self.getMotorsStatus()]

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

    def backup(self):

        try:

            if not os.path.exists(self.backupDir):

                os.mkdir(self.backupDir)

            backup_name = f"backup_{self.dataLog.getDate()}_at_{self.dataLog.getTime().replace(':','_')}_by_{self.dataLog.getUser()}"

            backup_adress = os.path.join(self.backupDir, backup_name)

            if not os.path.exists('./Logs'):
                raise Exception("No hay logs para hacer backup.")

            shutil.copytree("./Logs", backup_adress)

        except Exception as e:

            raise e

    def disconnectAllClients(self):

        self.workingID = None
        self.dataLog.logDisconnectAllClients()
        return "Todos los clientes desconectados."