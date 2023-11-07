import serial

class Serial:

    def __init__(self, puerto, baudrate):

        self.port = puerto
        self.baudrate = baudrate
        self.ser = None
        self.beginSerial()

    def __del__(self):

        self.stopSerial()

    def getData(self):

        return [self.port, self.baudrate]

    def beginSerial(self):

        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=5)

        except Exception as e:

            raise e

    def stopSerial(self):

        try:
            if self.ser is not None:
                self.ser.close()

        except Exception as e:

            raise e

    def writeSerial(self, mensaje):

        mensaje = (mensaje+"\r\n").encode()

        try:

            self.ser.write(mensaje)

        except Exception as e:

            raise e

    def readSerial(self):

        try:

            response = self.ser.readline().decode("utf-8", errors="ignore").replace("\r\n", "")
            return response

        except Exception as e:

            raise e

    def flushInput(self):

        try:

            self.ser.flushInput()

        except Exception as e:

            raise e