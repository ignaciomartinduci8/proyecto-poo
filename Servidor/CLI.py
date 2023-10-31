from Controlador import Controlador
from Servidor import Servidor
from cmd import Cmd


GREEN = "\033[92m"
RESET = "\033[0m"
ROJO = "\033[91m"
LIGHT_BLUE = "\033[94m"


class CLI(Cmd):

    doc_header = "Ayuda de comandos documentados"
    undoc_header = "Ayuda de comandos no documentados"
    ruler = "="

    def __init__(self):
        super().__init__()
        self.completekey = 'Tab'
        self.servidor1 = None
        self.controlador = Controlador()


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

            self.controlador.connect(puerto, baudrate)

        except ValueError:

            print(f"{ROJO}Error - argumentos inválidos.{RESET}")

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
