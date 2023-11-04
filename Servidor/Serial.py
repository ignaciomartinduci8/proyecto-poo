import serial

class Serial:

    def __init__(self, puerto, baudrate):

        self.port = puerto
        self.baudrate = baudrate
        self.ser = None
        self.beginSerial()

    def __del__(self):

        self.stopSerial()

    def beginSerial(self):

        try:

            self.ser = serial.Serial(self.port, self.baudrate)

        except Exception as e:

            raise e

    def stopSerial(self):

        try:

            if self.ser != None:
                self.ser.close()

        except Exception as e:

            raise e

    def writeSerial(self, mensaje):

        mensaje = mensaje.encode()

        try:

            self.ser.write(mensaje)

        except Exception as e:

            raise e

    def readSerial(self):

        response = self.ser.readline().decode().strip()
        return response
