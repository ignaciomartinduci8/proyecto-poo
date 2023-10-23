from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
import socket
from Controlador import Controlador

class Servidor:

    def __init__(self):

        self.open = False
        self.hostname = None
        self.port = None
        self.IP = None
        self.server_thread = None
        self.server = None

    def prueba(self, a,b):

        return a+b

    def abrirServidor(self, port):

        if self.open:

                print(f"Error - el servidor RPC ya está abierto en el puerto {self.port}")
                return

        try:

            self.hostname = socket.gethostname()
            self.IP = socket.gethostbyname(self.hostname)
            self.port = int(port)

            self.server = SimpleXMLRPCServer((self.IP, self.port))

            self.open = True

            print(f"Servidor RPC en el puerto {self.port}...")

            self.server.register_function(self.prueba, "prueba")

#           server.serve_forever()

            self.server_thread = Thread(target=self.server.serve_forever)
            self.server_thread.start()

        except Exception as e:

            print(f"Error - {e}")

    def cerrarServidor(self):

        try:
            self.server.shutdown()
            self.server_thread.join(timeout=2)
            self.open = False
            self.port = None
            self.IP = None
            self.hostname = None
            print("Servidor RPC cerrado.")

        except Exception as e:

            print(f"Error - {e}")




