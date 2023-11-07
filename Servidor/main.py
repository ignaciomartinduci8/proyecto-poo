from CLI import CLI
from GUI import MainWindow
from PyQt5.QtWidgets import QApplication
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
            cli = CLI(user)
            cli.prompt = '--> '
            cli.cmdloop('Iniciando entrada de comandos. Usar help para ver comandos. \nAlgunos comandos tienen argumentos opcionales, simbolizados con *')
            cli = None

        elif UI == "GUI":
            print("Corriendo GUI...")
            app = QApplication(sys.argv)
            mainWindow = MainWindow()
            mainWindow.show()
            sys.exit(app.exec_())

        else:
            print("Opcion no valida.")


if __name__ == "__main__":

    main()