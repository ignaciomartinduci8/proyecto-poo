from CLI import CLI
import sys


def main():

    while True:
        UI = str.upper(input("Bienvenido. Ingrese 'CLI' para utilizar CLI o 'GUI' para utilizar GUI. Para salir, ingrese 'EXIT': "))
        user = 'ANONYMOUS'
        user = input("Enter username: ")

        if UI == "EXIT":
            sys.exit(1)

        elif UI == "CLI":
            print("Corriendo CLI...")
            cli = CLI(user, False)
            cli.prompt = '--> '
            cli.cmdloop('Iniciando entrada de comandos. Usar help para ver comandos. \nAlgunos comandos tienen argumentos opcionales, simbolizados con *')
            cli = None

        elif UI == "GUI":
            print("Corriendo CLI con GUI...")
            cli = CLI(user, True)
            cli.prompt = '--> '
            cli.cmdloop('Iniciando entrada de comandos. Usar help para ver comandos. \nAlgunos comandos tienen argumentos opcionales, simbolizados con *')
            cli = None

        else:
            print("Opcion no valida.")


if __name__ == "__main__":

    main()

