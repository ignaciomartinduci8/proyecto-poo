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
        self.dataLog = dataLog
        self.connection_semaphore = Semaphore(1)
        self.abrirServidor()

    def prueba(self, a, b):
        return a+b

    def listMethods(self):

        return self.server.system_listMethods()

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

            self.serverRegisteringFunctions()

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

    def getServerData(self):

        return [self.hostname, self.IP, self.port]

    def serverRegisteringFunctions(self):

        self.server.register_introspection_functions()

        self.server.register_function(self.prueba)
        self.server.register_function(self.listMethods)

    def __del__(self):

        self.cerrarServidor()