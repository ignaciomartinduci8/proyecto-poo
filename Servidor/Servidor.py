from xmlrpc.server import SimpleXMLRPCServer

class Servidor:


    def __init__(self):

        self.open = False


    def prueba(self, a,b):

        return a+b

    def abrirServidor(self):


        server = SimpleXMLRPCServer(("localhost", 8000))

        print("Servidor RPC en el puerto 8000...")

        server.register_function(prueba, "prueba")

        server.serve_forever()



