import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Mi Aplicación PyQt5')
        self.setGeometry(100, 100, 400, 200)

        label = QLabel('¡Hola, PyQt5!')

