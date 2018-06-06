import tkinter as tk

from PyQt5.QtWidgets import (QWidget, QPushButton, QMessageBox)

from src.level_dialog import LevelWindow

root = tk.Tk()


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.level = LevelWindow()
        self.init_ui()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def init_ui(self):
        """
        Начальная прорисовка окна
        """

        self.btn1 = QPushButton('Новая игра', self)
        self.btn1.clicked.connect(self.on_new_game_clicked)
        self.btn1.move(10, 10)
        self.btn1.resize(220, 30)

        self.btn2 = QPushButton('Об авторе', self)
        self.btn2.move(10, 50)
        self.btn2.resize(220, 30)

        self.btn3 = QPushButton('Выйти', self)
        self.btn3.clicked.connect(self.close)
        self.btn3.move(10, 90)
        self.btn3.resize(220, 30)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(screen_width // 2 - 120, screen_height // 2 - 180, 240, 360)
        self.setWindowTitle('Tooltips')
        self.show()

    def on_new_game_clicked(self):
        self.level.show()
        self.hide()
