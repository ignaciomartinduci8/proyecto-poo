from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread, Semaphore
import socket
from Controlador import Controlador

class Servidor:

    def __init__(self, port, dataLog):

        self.hostname = None
        self.port = port
        self.IP = None
        self.server_thread = None
        self.server = None
        self.clientName = None
        self.clientIP = None
        self.clientPort = None
        self.client_info = [] 
        self.dataLog = dataLog
        self.connection_semaphore = Semaphore(1)
        self.abrirServidor()

    def prueba(self, a, b):
        return a+b

    def loopConnection(self):
        with self.connection_semaphore:
            self.server.serve_forever()
        self.dataLog.logServerStatus(self.IP, self.port, True)

    def abrirServidor(self):

        try:

            self.hostname = socket.gethostname()
            self.IP = socket.gethostbyname(self.hostname)
            self.port = int(self.port)

            self.server = SimpleXMLRPCServer((self.IP, self.port))

            self.server.register_introspection_functions()

            self.server.register_function(self.setUsername,'setUsername')
            # Funciones de conexion
            self.server.register_function(self.controlador.connect,'connect')
            self.server.register_function(self.controlador.disconnect,'disconnect')
            
            # Funciones de movimiento del robot
            self.server.register_function(self.controlador.goHome,'goHome')
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
            self.server.register_function(self.controlador.goHome, 'goHome')
            self.server.register_function(self.controlador.getRobotStatus, 'getRobotStatus')
            self.server.register_function(self.controlador.report, 'report')
            self.server.register_function(self.controlador.backup, 'backup')

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
        return self.clientName

    def getUsername(self):
        return self.clientName

    #def close_client_connection(self):

    def getServerData(self):

        return [self.hostname, self.IP, self.port]
    
    def __del__(self):

        self.cerrarServidor()
