from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
import socket
from Controlador import Controlador


class Servidor:

    def __init__(self, port):

        self.hostname = None
        self.port = port
        self.IP = None
        self.server_thread = None
        self.server = None
        self.abrirServidor()

    def prueba(self, a, b):
        return a+b

    def listMethods(self):

        return self.server.system_listMethods()

    def abrirServidor(self):

        try:

            self.hostname = socket.gethostname()
            self.IP = socket.gethostbyname(self.hostname)
            self.port = int(self.port)

            self.server = SimpleXMLRPCServer((self.IP, self.port))

            self.server.register_function(self.listMethods, "listMethods")
            self.server.register_function(self.prueba, "prueba")

#           server.serve_forever()

            self.server_thread = Thread(target=self.server.serve_forever)
            self.server_thread.start()

        except Exception as e:

            raise e

    def cerrarServidor(self):

        try:
            self.server.shutdown()
            self.server_thread.join(timeout=2)

        except Exception as e:

            raise e

    def getServerData(self):

        return [self.hostname, self.IP, self.port]


