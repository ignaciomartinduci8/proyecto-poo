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

            self.ser.close()

        except Exception as e:

            raise e

    def writeSerial(self):

            try:

                mensaje = "Hola"
                self.ser.write(mensaje.encode())

            except Exception as e:

                raise e