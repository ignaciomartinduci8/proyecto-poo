from Serial import Serial
from Robot import Robot

class Controlador:

    def __init__(self, dataLog):
        self.isConnected = False
        self.serial = None
        self.robot = None
        self.dataLog = dataLog

    def connect(self, puerto, baudrate):

        try:
            self.serial = Serial(puerto, baudrate)
            self.robot = Robot("Robot POO - Grupo Negro")
            self.isConnected = True

        except Exception as e:

            raise e

    def disconnect(self):

        try:

            self.serial.cerrarSerial()
            self.isConnected = False

        except Exception as e:

            raise e

    def getIsConnected(self):

        return self.isConnected

    def setRobotMode(self, mode):

        if not self.isConnected:

            raise Exception("No hay robot conectado")

        try:

            self.robot.setMode(mode)

        except Exception as e:

            raise e





