from Serial import Serial
from Robot import Robot

class Controlador:

    def __init__(self):
        self.isConnected = False
        self.serial = None
        self.robot = None

    def connect(self, puerto, baudrate):

        try:
            self.serial = Serial(puerto, baudrate)
            self.robot = Robot()
            self.isConnected = True

        except Exception as e:

            raise e