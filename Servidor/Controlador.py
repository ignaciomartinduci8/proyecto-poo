from Serial import Serial
from Robot import Robot

class Controlador:

    def __init__(self, dataLog):
        self.isConnected = False
        self.isRobotInUse = False  # Variable de bloqueo
        self.serial = None
        self.robot = None
        self.dataLog = dataLog

    def lockRobot(self):
        self.isRobotInUse = True

    def unlockRobot(self):
        self.isRobotInUse = False

    def connect(self, puerto, baudrate):
        if self.isRobotInUse:
            raise Exception("El robot está siendo controlado por otro usuario. Por favor, espere.")
        
        try:
            self.lockRobot()  # Bloquear el robot
            self.serial = Serial(puerto, baudrate, self.robot)
            connectMessage = self.serial.readSerial()
            self.robot = Robot("Robot POO - Grupo Negro", self.serial)
            self.isConnected = True
            return connectMessage
        except Exception as e:
            self.unlockRobot()  # Desbloquear el robot en caso de excepción
            raise e

    def disconnect(self):
        if self.isRobotInUse:
            raise Exception("El robot está siendo controlado por otro usuario. Por favor, espere.")
        try:
            self.unlockRobot()  # Desbloquear el robot antes de desconectar
            del self.serial
            self.isConnected = False
        except Exception as e:
            raise e

    def getIsConnected(self):
        return self.isConnected

    def setRobotMode(self, mode):
        if self.isRobotInUse:
            raise Exception("El robot está siendo controlado por otro usuario. Por favor, espere.")
        if not self.isConnected:
            raise Exception("No se ha conectado un robot.")
        try:
            self.robot.setMode(mode)
        except Exception as e:
            raise e

    def moveEffector(self, x, y, z, al, be, ga, s_max=None):
        if self.isRobotInUse:
            raise Exception("El robot está siendo controlado por otro usuario. Por favor, espere.")
        if self.robot.getMode() != 'M':
            raise Exception('Operación no válida, robot en modo automático')
        if not self.isConnected:
            raise Exception("Error - No se ha conectado un robot.")
        try:
            self.robot.setPosture(x, y, z, al, be, ga, s_max)
        except Exception as e:
            raise e

    def enableEffector(self):
        if self.isRobotInUse:
            raise Exception("El robot está siendo controlado por otro usuario. Por favor, espere.")
        if self.robot.getMode() != 'M':
            raise Exception('Operación no válida, robot en modo automático.')
        if not self.isConnected:
            raise Exception("No se ha conectado un robot.")
        if self.robot.getEffectorStatus():
            raise Exception('Ya se ha activado el effector.')
        try:
            self.robot.enableEffector()
        except Exception as e:
            raise e

    def disableEffector(self):
        if self.isRobotInUse:
            raise Exception("El robot está siendo controlado por otro usuario. Por favor, espere.")
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
        if self.isRobotInUse:
            raise Exception("El robot está siendo controlado por otro usuario. Por favor, espere.")
        if not self.isConnected:
            raise Exception("No se ha conectado un robot.")
        self.robot.getEffectorStatus()

    def getPosture(self):
        return self.robot.getPosture()

    def setMappingQuality(self, quality):
        if self.isRobotInUse:
            raise Exception("El robot está siendo controlado por otro usuario. Por favor, espere.")
        if not self.isConnected:
            raise Exception("No se ha conectado un robot.")
        try:
            self.robot.setMappingQuality(quality)
        except Exception as e:
            raise e
