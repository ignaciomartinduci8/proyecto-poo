from Controlador import Controlador
from Servidor import Servidor
from DataLog import DataLog
from cmd import Cmd
import tkinter as tk
from tkinter import messagebox


GREEN = "\033[92m"
RESET = "\033[0m"
ROJO = "\033[91m"
LIGHT_BLUE = "\033[94m"
IDENTATION = f"{LIGHT_BLUE}>{RESET}"


class CLI(Cmd):

    doc_header = "Ayuda de comandos documentados"
    undoc_header = "Ayuda de comandos no documentados"
    ruler = "="

    def __init__(self, user):
        super().__init__()
        self.completekey = 'tab'
        self.servidor1 = None
        self.dataLog = DataLog(user)
        self.controlador = Controlador(self.dataLog)
        self.serverUser = user
        self.dataLog.logProgram(True)

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
                    self.servidor1 = Servidor(puerto, self.dataLog,self.controlador)
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
        self.dataLog.logProgram(False)
        print("Cerrando programa...")
        raise SystemExit

    def do_connectSerial(self, args):
        """
        Descripción: Conectar a un Robot en puerto serie
        Sintaxis: connectSerial [puerto] [baudrate]

        """

        try:

            puerto, baudrate = args.split(" ")

            res = self.controlador.connect(puerto, baudrate, "ADMIN")
            print(f"{GREEN}Respuesta del proceso:{RESET}")

            for i in res:
                print(f"{IDENTATION}{i}{RESET}")

            print(f"{IDENTATION}Robot conectado en puerto {puerto} a {baudrate} baudios.")

        except ValueError:

            print(f"{ROJO}Error - argumentos inválidos.{RESET}")

        except Exception as e:

            print(f"{ROJO}Error - {e}{RESET}")

    def do_disconnectSerial(self, args):
        """
            Descripción: Desconectar a un Robot en puerto serie
            Sintaxis: disconnectSerial

        """

        try:

            res = self.controlador.disconnect("ADMIN")
            print(f"{GREEN}Respuesta del proceso:{RESET}")
            print(f"{IDENTATION}{res}{RESET}")

        except Exception as e:

            print(f"{ROJO}Error - {e}{RESET}")

    def do_goHome(self, args):
        """
            Descripción: Mover robot a posición de inicio
            Sintaxis: goHome

        """

        try:

            res = self.controlador.goHome("ADMIN")
            print(f"{GREEN}Respuesta del proceso:{RESET}")

            for i in range(4):
                print(f"{IDENTATION}{res[i]}{RESET}")

        except Exception as e:

            print(f"{ROJO}Error - {e}{RESET}")

    def do_moveEffector(self, args):
        """
            Descripción: Mover efector final
            Sintaxis: moveEffector [x] [y] [z] [s_max*]

        """

        try:

            args = args.split(" ")

            if len(args) == 4:
                res = self.controlador.moveEffector(args[0], args[1], args[2], args[3],"ADMIN")
            elif len(args) == 3:
                res = self.controlador.moveEffector(args[0], args[1], args[2],"ADMIN")

            else:
                print(f"{ROJO}Error - argumentos inválidos.{RESET}")
                return

            print(f"{GREEN}Respuesta del proceso:{RESET}")
            print(f"{IDENTATION}{res}")

        except ValueError:

            print(f"{ROJO}Error - argumentos inválidos.{RESET}")

        except Exception as e:

            if "OUTSIDE" in str(e):

                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Error", "Posición fuera de rango.")
                root.lift()
                root.focus_force()
                root.destroy()

            print(f"{ROJO}Error - {e}{RESET}")

    def do_setRobotMode(self, args):
        """
            Descripción: Establecer modo de trabajo manual o automático
            Sintaxis: setRobotMode [M/A]

        """

        args = args.upper()

        if len(args) != 1:
            print(f"{ROJO}Error - argumentos inválidos.{RESET}")

        try:

            if args == "M":

                if self.controlador.getRobotStatus()[0] == "M":
                    print(f"{ROJO}Error - El robot ya está en modo manual.{RESET}")
                    return

                res = self.controlador.setRobotMode(args,"ADMIN")
                print(f"{GREEN}Respuesta del proceso:{RESET}")

                for i in range(5):
                    print(f"{IDENTATION}{res[i]}{RESET}")

            elif args == "A":

                if self.controlador.getRobotStatus()[0] == "A":
                    print(f"{ROJO}Error - El robot ya está en modo automático.{RESET}")
                    return

                files = self.controlador.listAutomaticFiles()

                if len(files) == 0:
                    print(f"{ROJO}Error - No hay archivos de modo automático disponibles.{RESET}")
                    return

                print(f"{GREEN}Archivos disponibles:{RESET}")

                for file in files:
                    print(f"{IDENTATION}{file}{RESET}")

                file = input(f"Ingrese el nombre del archivo a ejecutar: ")

                self.controlador.setRobotMode('A', file,"ADMIN")

            else:

                print(args)
                print(f"{ROJO}Error - Modo no existente.{RESET}")

        except ValueError:

            print(f"{ROJO}Error - argumentos inválidos.{RESET}")

        except TypeError:

            print(f"{ROJO}Error - argumentos inválidos.{RESET}")

        except Exception as e:

            print(f"{ROJO}Error - {e}{RESET}")

    def do_enableEffector(self, args):
        """
            Descripción: Activar efector final
            Sintaxis: enableEffector

        """


        try:

            res = self.controlador.enableEffector("ADMIN")

            print(f"{GREEN}Respuesta del proceso:{RESET}")
            print(f"{IDENTATION}{res}")

        except Exception as e:

            print(f"{ROJO}Error - {e}{RESET}")

    def do_disableEffector(self, args):
        """
            Descripción: Desactivar efector final
            Sintaxis: disableEffector

        """

        try:

            self.controlador.disableEffector("ADMIN")
            print(f"{GREEN}Respuesta del proceso:{RESET}")
            print(f"{IDENTATION}Efector desactivado.{RESET}")

        except Exception as e:

            print(f"{ROJO}Error - {e}{RESET}")

    def do_enableMotors(self, args):
        """
            Descripción: Activar motores
            Sintaxis: enableMotors

        """

        try:

            res = self.controlador.enableMotors("ADMIN")
            print(f"{GREEN}Respuesta del proceso:{RESET}")
            print(f"{IDENTATION}{res}")

        except Exception as e:

            print(f"{ROJO}Error - No se ha podido activar los motores{RESET}")

    def do_disableMotors(self, args):
        """
            Descripción: Desactivar motores
            Sintaxis: disableMotors

        """

        try:

            res = self.controlador.disableMotors("ADMIN")
            print(f"{GREEN}Respuesta del proceso:{RESET}")
            print(f"{IDENTATION}{res}")

        except Exception as e:

            print(f"{ROJO}Error - {e}{RESET}")

    def do_getRobotStatus(self, args):

        """
            Descripción: Obtener estado del robot
            Sintaxis: getRobotStatus

        """

        try:

            res = self.controlador.getRobotStatus()
            print(f"{GREEN}Respuesta del proceso:{RESET}")

            print(f"{IDENTATION}Modo: {res[0]}{RESET}")
            print(f"{IDENTATION}Posición: X:{res[1][0]} mm Y:{res[1][1]} mm Z:{res[1][2]}{RESET} mm")
            print(f"{IDENTATION}Efector: {res[2]}{RESET}")
            print(f"{IDENTATION}Motores: {res[3]}{RESET}")

        except Exception as e:

            print(f"{ROJO}Error - {e}{RESET}")

    def do_generalReport(self, args):
        """
        Descripción: Obtener estado del robot
        Sintaxis: report
        """

        try:

            res = self.controlador.report()

            print(f"{GREEN}Respuesta del proceso:{RESET}")

            for i in res:
                print(f"{IDENTATION}{i}{RESET}")

        except Exception as e:
            print(f"{ROJO}Error - {e}{RESET}")

    def do_listAutomaticFiles(self, args):
        """
        Descripción: Listar archivos de modo automático
        Sintaxis: listAutomaticFiles
        """

        try:

            res = self.controlador.listAutomaticFiles()

            print(f"{GREEN}Respuesta del proceso:{RESET}")

            for i in res:
                print(f"{IDENTATION}{i}{RESET}")

        except Exception as e:
            print(f"{ROJO}Error - {e}{RESET}")
    
    def do_toggleLearn(self, args):
        """
        Descripción: Activar/desactivar modo aprendizaje
        Sintaxis: toggleLearn [S/N] [*filename]
        """
        args = args.split(" ")

        if len(args) == 1:
            onOff = args[0]
            filename = None

        elif len(args) == 2:
            onOff = args[0]
            filename = args[1]

        else:
            print(f"{ROJO}Error - argumentos inválidos.{RESET}")

        try:

            res = self.controlador.toggleLearn(onOff, filename, "ADMIN")

            print(f"{GREEN}Respuesta del proceso:{RESET}")
            print(f"{IDENTATION}{res}{RESET}")

        except Exception as e:

            print(f"{ROJO}Error - {e}{RESET}")

    def do_backup(self, args):

        print(f"{GREEN}Respuesta del proceso:{RESET}")
        print(f"{IDENTATION}Realizando backup...{RESET}")
        self.controlador.backup()
        print(f"{IDENTATION}Backup realizado.{RESET}")

    def do_disconnectAllClients(self):
        """
        Descripción: Desconectar todos los clientes
        Sintaxis: disconnectAllClients
        """

        try:

            res = self.controlador.disconnectAllClients("ADMIN")

            print(f"{GREEN}Respuesta del proceso:{RESET}")
            print(f"{IDENTATION}{res}{RESET}")

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
            print("=========================================================================================================================")
            cmds = []
            for attr in dir(self):
                if attr.startswith("do_"):
                    cmd_name = attr[3:]
                    cmds.append(cmd_name)

            cmds.sort()
            cmd_buffer = []
            count = 0

            for cmd_name in cmds:

                cmd_buffer.append(f" --> {GREEN}{cmd_name}{RESET}")
                count += 1
                if count == 7 or cmd_name == cmds[-1]:
                    print("".join(cmd_buffer))
                    cmd_buffer = []
                    count = 0

            print(f"\nEscribe 'help {GREEN}[comando]{RESET}' para obtener ayuda sobre un comando específico.")
            print("=========================================================================================================================\n")

    def precmd(self, args):

        self.do_help(None)

        return args

    def preloop(self):
        print('\n========== CLI de servidor ==========')
        self.do_help(None)


