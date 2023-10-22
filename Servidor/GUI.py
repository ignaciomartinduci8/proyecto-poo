import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QMainWindow, QLabel
import pyautogui


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.screen_width, self.screen_height = pyautogui.size()  # Get the screen size
        self.initUI()
        self.raise_()


    def initUI(self):

        self.setWindowTitle('Proyecto POO - GUI')
        print(f"Screen height: {self.screen_height}")
        print(f"Screen width: {self.screen_width}")
        self.setGeometry(round(self.screen_width/4), round(self.screen_height/4), round(self.screen_width/2), round(self.screen_height/2))

        label = QLabel('Hello, PyQt5!', self)
        label.move(round(self.screen_width/8), round(self.screen_height/8))  # Set label position

        button = QPushButton('Click Me!', self)
        button.move(round(self.screen_width/8), round(self.screen_height/8)+50)  # Set button position
        button.clicked.connect(self.onButtonClick)  # Connect button click event to a method


    def onButtonClick(self):
        print('Button clicked!')
