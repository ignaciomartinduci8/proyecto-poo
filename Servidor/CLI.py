from Controlador import Controlador
from Servidor import Servidor
from DataLog import DataLog
from cmd import Cmd


GREEN = "\033[92m"
RESET = "\033[0m"
ROJO = "\033[91m"
LIGHT_BLUE = "\033[94m"
IDENTATION = f"{LIGHT_BLUE}>{RESET}      "


class CLI(Cmd):

    doc_header = "Ayuda de comandos documentados"
    undoc_header = "Ayuda de comandos no documentados"
    ruler = "="

    def __init__(self):
        super().__init__()
        self.completekey = 'Tab'
        self.servidor1 = None
        self.dataLog = DataLog()
        self.controlador = Controlador(self.dataLog)

    def do_RPCon(self, puerto):
        """
        Descripción: Abre el servidor RPC
        Sintaxis: RCPon [puerto]

        """

        try:

            puerto = int(puerto)

            # Control de errores de rango de argumentos
            if puerto < 1024 or puerto > 65535:
                print(f"{ROJO}Error en el puerto, debe estar entre 1025 y 65535. Motivos de seguridad y existencia.{RESET}")
                return

            if self.servidor1 is None:

                try:
                    self.servidor1 = Servidor(puerto)
                    print(f"Servidor RPC abierto en el puerto {puerto}.")

                except Exception as e:

                    if "10013" in str(e):

                        print(f"{ROJO}Error - el puerto {puerto} está en uso.{RESET}")

                    else:

                        print(f"{ROJO}Error - {e}{RESET}")

            else:

                print(f"{ROJO}Error - el servidor ya está abierto. En el puerto {self.servidor1.getServerData()[2]}{RESET}")

        except ValueError:
            print(f"{ROJO}Error - el puerto debe ser un número entero válido.{RESET}")

        except Exception as e:
            print(f"{ROJO}Error inesperado - {e}{RESET}")

    def do_RPCoff(self, args):
        """
        Descripción: Cierra el servidor RPC
        Sintaxis: RCPoff [mensaje]
        """

        try:
            self.servidor1.cerrarServidor()
            print(f"Servidor cerrado. Puerto {self.servidor1.getServerData()[2]} liberado.")
            self.servidor1 = None

        except Exception as e:
            print(f"{ROJO}Error - {e}{RESET}")

    def default(self, args):
        print(f"{ROJO}Error, el comando /{args} no existe.{RESET}")

    def do_exit(self, args):
        """
        Descripción: Cierra el programa
        Sintaxis: exit
        """
        print("Cerrando programa...")
        raise SystemExit

    def do_connectSerial(self, args):
        """
        Descripción: Conectar a un Robot en puerto serie
        Sintaxis: connectSerial [puerto] [baudrate]

        """

        try:

            puerto, baudrate = args.split(" ")

            response = self.controlador.connect(puerto, baudrate)
            print(f"{GREEN}Respuesta del proceso:{RESET}")
            print(f"{IDENTATION}{response}")
            print(f"{IDENTATION}Robot conectado en puerto {puerto} a {baudrate} baudios.")

            posture = self.controlador.getPosture()
            print(f"{IDENTATION}El robot viajó a su posición de inicio.")
            print(f"{IDENTATION}Posición actual: [{posture[0]}, {posture[1]}, {posture[2]}]\n"
                  f"{IDENTATION}Orientación actual: [{posture[3]}, {posture[4]}, {posture[5]}]")

        except ValueError:

            print(f"{ROJO}Error - argumentos inválidos.{RESET}")

        except Exception as e:

            print(f"{ROJO}Error - {e}{RESET}")

    def do_disconnectSerial(self, args):
        """
            Descripción: Desconectar a un Robot en puerto serie
            Sintaxis: disconnectSerial

        """

        if self.controlador.getIsConnected():

            try:

                self.controlador.disconnect()
                print("Robot desconectado.")

            except Exception as e:

                print(f"{ROJO}Error - {e}{RESET}")

        else:

            print(f"{ROJO}Error - no hay conexión establecida.{RESET}")

    def do_moveEffector(self, args):
        """
            Descripción: Mover efector final
            Sintaxis: moveEffector [x] [y] [z] [al] [be] [ga] [s_max*]

        """

        try:

            args = args.split(" ")

            if len(args) == 7:
                self.controlador.moveEffector(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
            elif len(args) == 6:
                self.controlador.moveEffector(args[0], args[1], args[2], args[3], args[4], args[5])

            else:
                print(f"{ROJO}Error - argumentos inválidos.{RESET}")
                return


            print("Movimiento realizado correctamente.")
            posture = self.controlador.getPosture()
            print(f"Posición actual: [{posture[0]}, {posture[1]}, {posture[2]}]\n"
                  f"Orientación actual: [{posture[3]}, {posture[4]}, {posture[5]}]")

        except ValueError:

            print(f"{ROJO}Error - argumentos inválidos.{RESET}")

        except Exception as e:

            print(f"{ROJO}Error - {e}{RESET}")

    def do_setRobotMode(self, args):
        """
            Descripción: Establecer modo de trabajo manual o automático
            Sintaxis: setRobotMode [M/A]

        """
        if args == "M" or args == "A":

            try:

                self.controlador.setRobotMode(args)
                print(f'Modo {args} establecido correctamente.')

            except Exception as e:

                print(f"{ROJO}Error - {e}{RESET}")

        else:

            print(f"{ROJO}Error - modo inválido.{RESET}")

    def do_enableEffector(self,args):
        """
            Descripción: Activar efector final
            Sintaxis: enableEffector

        """

        try:

            self.controlador.enableEffector()
            print("Efector activado.")

        except Exception as e:

            print(f"{ROJO}Error - {e}{RESET}")

    def do_disableEffector(self, args):
        """
            Descripción: Desactivar efector final
            Sintaxis: disableEffector

        """

        try:

            self.controlador.disableEffector()
            print("Efector desactivado.")

        except Exception as e:

            print(f"{ROJO}Error - {e}{RESET}")

    def do_setMappingQuality(self, args):

        """
            Descripción: Establecer calidad de mapeo
            Sintaxis: setMappingQuality [calidad]

        """

        if len(args.split(" ")) > 1:

                print(f"{ROJO}Error - argumentos inválidos.{RESET}")
                return

        try:

            self.controlador.setMappingQuality(args)
            print(f"Calidad de mapeo establecida en {args}.")

        except Exception as e:

            print(f"{ROJO}Error - {e}{RESET}")

    def do_help(self, args):
        """
        Descripción: Obtener ayuda
        Sintaxis: help
        """

        if args:
            cmd_func = getattr(self, 'do_' + args, None)
            if cmd_func:
                print(f'\n{GREEN}{args}{RESET}: {cmd_func.__doc__ or "Sin descripción"}')
            else:
                print(f'{ROJO}\nError: El comando {args} no existe.{RESET}')
        else:

            print('\n' + self.doc_header)
            print("=============================")
            cmds = []
            for attr in dir(self):
                if attr.startswith("do_"):
                    cmd_name = attr[3:]
                    cmds.append(cmd_name)

            cmds.sort()
            for cmd_name in cmds:
                print(f" --> {GREEN}{cmd_name}{RESET}")
            print(f"\nEscribe 'help {GREEN}[comando]{RESET}' para obtener ayuda sobre un comando específico.")

    def precmd(self, args):
        return args

    def preloop(self):
        print('\n========== CLI de servidor ==========')
