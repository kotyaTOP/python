import tkinter as tk

from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QMessageBox)

from src.game_dialog import GameWindow
from src.model.field import Field
from src.presenter.presenter import Presenter

root = tk.Tk()


class LevelWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.levels = [GameWindow(), GameWindow(), GameWindow()]
        self.levels[0].presenter = Presenter(Field(5, 5), self.levels[0])
        self.levels[1].presenter = Presenter(Field(10, 7), self.levels[1])
        self.levels[2].presenter = Presenter(Field(14, 10), self.levels[2])
        self.init_ui()

    def closeEvent(self, event):
        """
        @Deprecated
        Обработка закрытия окна
        :param event:
        :return:
        """

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def init_ui(self):
        btn = QPushButton('1', self)
        btn.clicked.connect(self.on_level_clicked_0)
        btn.move(20, 10)
        btn.resize(50, 30)

        btn = QPushButton('2', self)
        btn.clicked.connect(self.on_level_clicked_1)
        btn.move(80, 10)
        btn.resize(50, 30)

        btn = QPushButton('3', self)
        btn.clicked.connect(self.on_level_clicked_2)
        btn.move(140, 10)
        btn.resize(50, 30)

        btn = QPushButton('Выйти', self)
        btn.clicked.connect(QApplication.instance().quit)
        btn.move(10, 50)
        btn.resize(220, 30)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(screen_width // 2 - 120, screen_height // 2 - 180, 240, 360)
        self.setWindowTitle('Tooltips')

    def on_level_clicked_0(self):
        self.levels[0].presenter.start()
        self.levels[0].show()
        self.hide()

    def on_level_clicked_1(self):
        self.levels[1].presenter.start()
        self.levels[1].show()
        self.hide()

    def on_level_clicked_2(self):
        self.levels[2].presenter.start()
        self.levels[2].show()
        self.hide()


    def on_level_clicked(self, n: int):
        self.levels[n].presenter.start()
        self.levels[n].show()
        self.hide()
