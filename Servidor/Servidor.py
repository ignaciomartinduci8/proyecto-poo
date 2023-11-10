import time
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Thread
import socket
from DataLog import DataLog


class CustomXMLRPCServer(SimpleXMLRPCServer):

    def __init__(self, *args, **kwargs):
        SimpleXMLRPCServer.__init__(self, *args, **kwargs)
        self.clientIP = None
        self.clientPort = None


    def finish_request(self, request, client_address):
        print("Client connected from:", client_address)

        self.clientIP = client_address[0]
        self.clientPort = client_address[1]

        SimpleXMLRPCServer.finish_request(self, request, client_address)

    def getDataClient(self):

        return [self.clientIP, self.clientPort]


class Servidor:

    def __init__(self, port, dataLog, controlador):

        self.hostname = None
        self.port = port
        self.IP = None
        self.server_thread = None
        self.server = None
        self.dataLog = dataLog
        self.controlador = controlador
        self.abrirServidor()
        self.clientName = None
        self.clientIP = None
        self.clientPort = None

    def prueba(self, a, b):
        return a + b

    def loopConnection(self):

        self.dataLog.logServerStatus(self.IP, self.port, True)
        self.server.serve_forever()

    def abrirServidor(self):

        try:

            self.hostname = socket.gethostname()
            self.IP = socket.gethostbyname(self.hostname)
            self.port = int(self.port)

            self.server = CustomXMLRPCServer((self.IP, self.port),logRequests=False, allow_none=True)

            self.server.register_introspection_functions()

            self.server.register_function(self.setUsername, 'setUsername')
            # Funciones de conexion
            self.server.register_function(self.controlador.connect, 'connectSerial')
            self.server.register_function(self.controlador.disconnect, 'disconnectSerial')

            # Funciones de movimiento del robot
            self.server.register_function(self.controlador.goHome, 'goHome')
            self.server.register_function(self.controlador.setRobotMode, 'setRobotMode')
            self.server.register_function(self.controlador.manualMode, 'manualMode')
            self.server.register_function(self.controlador.listAutomaticFiles, 'listAutomaticFiles')
            self.server.register_function(self.controlador.automaticMode, 'automaticMode')
            self.server.register_function(self.controlador.runAutomaticFile, 'runAutomaticFile')
            self.server.register_function(self.controlador.learnAutomaticFile, 'learnAutomaticFile')
            self.server.register_function(self.controlador.toggleLearn, 'toggleLearn')
            self.server.register_function(self.controlador.moveEffector, 'moveEffector')
            self.server.register_function(self.controlador.enableEffector, 'enableEffector')
            self.server.register_function(self.controlador.disableEffector, 'disableEffector')
            self.server.register_function(self.controlador.getRobotStatus, 'getRobotStatus')
            self.server.register_function(self.controlador.enableMotors, 'enableMotors')
            self.server.register_function(self.controlador.disableMotors, 'disableMotors')
            self.server.register_function(self.controlador.report, 'report')

            self.server_thread = Thread(target=self.loopConnection)
            self.server_thread.start()

        except Exception as e:

            raise e

    def cerrarServidor(self):

        try:
            self.server.shutdown()
            self.server_thread.join(timeout=2)
            self.dataLog.logServerStatus(self.IP, self.port, False)

        except Exception as e:

            raise e

    def setUsername(self, username):
        self.clientName = username
        self.clientIP, self.clientPort = self.server.getDataClient()
        self.dataLog.logRPCClientConnected(self.clientIP, self.clientPort, self.clientName)
        return f"Bievenido al servicio RPC: {username}"

    def getUsername(self):
        return self.clientName

    def getServerData(self):

        return [self.hostname, self.IP, self.port]

    def __del__(self):

        self.cerrarServidor()
