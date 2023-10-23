from xmlrpc.server import SimpleXMLRPCServer
import threading
import socket
import errno

class Servidor:

    def __init__(self):

        self.open = False
        self.port = None


    def prueba(self, a,b):

        return a+b

    def abrirServidor(self, port):

        if self.open:

                print(f"Error - el servidor RPC ya está abierto en el puerto {self.port}")
                return

        try:

            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)

            print(f"Hostname: {hostname} | IP: {ip_address}")

            server = SimpleXMLRPCServer((ip_address, port))
            self.open = True
            self.port = port

            print(f"Servidor RPC en el puerto {self.port}...")

            server.register_function(self.prueba, "prueba")

#           server.serve_forever()

            server_thread = threading.Thread(target=server.serve_forever)

        except Exception as e:

            print(f"Error - {e}")






