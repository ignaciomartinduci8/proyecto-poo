import serial

class Serial:

    def __init__(self, puerto, baudrate):

        self.puerto = puerto
        self.baudrate = baudrate
        self.ser = None
        self.abrirSerial()

    def abrirSerial(self):

        try:

            self.ser = serial.Serial(self.puerto, self.baudrate)

        except Exception as e:

            raise e

    def cerrarSerial(self):

        try:

            self.ser.close()

        except Exception as e:

            raise e

