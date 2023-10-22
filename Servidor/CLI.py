
from cmd import Cmd
GREEN = "\033[92m"
RESET = "\033[0m"
LIGHT_BLUE = "\033[94m"


class CLI(Cmd):

    doc_header = "Ayuda de comandos documentados"
    undoc_header = "Ayuda de comandos no documentados"
    ruler = "="

    def __init__(self):
        super().__init__()
        self.completekey = 'Tab'
        self.file_name = None
        self.current_object = None

    def do_RPCon(self, args):
        """
        Descripción: Abre el servidor RCP
        Sintaxis: RCPon [puerto]
        """

    def do_RPCoff(self, args):
        """
        Descripción: Cierra el servidor RCP
        Sintaxis: RCPoff [mensaje]
        """

    def default(self, args):
        print("Error, el comando /"+args+" no existe.")

    def do_exit(self, args):
        """
        Descripción: Cierra el programa
        Sintaxis: exit
        """
        print("Cerrando programa...")
        raise SystemExit

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
                print(f'\nError: El comando {GREEN}{args}{RESET} no existe.')
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
