from CLI import CLI
from GUI import GUI
import sys


def main():

    while True:
        user = input("Bienvenido. Ingrese su nombre de usuario: ")
        UI = str.upper(input("Ingrese 'CLI' para utilizar CLI o 'GUI' para utilizar GUI. Para salir, ingrese 'EXIT': "))


        if UI == "EXIT":
            sys.exit(1)

        elif UI == "CLI":
            print("Corriendo CLI...")
            cli = CLI(user)
            cli.prompt = '--> '
            cli.cmdloop('Iniciando entrada de comandos. Usar help para ver comandos. \nAlgunos comandos tienen argumentos opcionales, simbolizados con *')
            cli = None

        elif UI == "GUI":
            print("Corriendo GUI...")
            gui = GUI(user)

        else:
            print("Opcion no valida.")


if __name__ == "__main__":

    main()

