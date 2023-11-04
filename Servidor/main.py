from CLI import CLI
from GUI import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

def main():
    while True:
        UI = str.upper(input("Bienvenido. Ingrese 'CLI' para utilizar CLI o 'GUI' para utilizar GUI. Para salir, ingrese 'EXIT': "))
        
        if UI == "EXIT":
            break
        elif UI == "CLI":
            print("Corriendo CLI...")
            cli = CLI()
            cli.prompt = '--> '
            cli.cmdloop('Iniciando entrada de comandos. Usar help para ver comandos. \nAlgunos comandos tienen argumentos opcionales, simbolizados con *')
        elif UI == "GUI":
            print("Corriendo GUI...")
            app = QApplication(sys.argv)
            mainWindow = MainWindow()
            mainWindow.show()
            sys.exit(app.exec_())
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
