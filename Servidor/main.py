from CLI import CLI
from GUI import MainWindow
from PyQt5.QtWidgets import QApplication
import sys


def main():

    UI = str.upper(input("Enter 'CLI' for CLI or 'GUI' for GUI: "))

    if UI == "CLI":

        print("Corriendo CLI...")
        cli = CLI()
        cli.prompt = '--> '
        cli.cmdloop('Iniciando entrada de comandos. Usar help para ver comandos.')

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
