import os

from src.model.field import *
from src.presenter.presenter import Presenter
from src.view.gamewindow import GameWindow, QMessageBox, QButtonGroup, QCheckBox


class Game:
    def __init__(self) -> None:
        super().__init__()
        self.levels = dict()
        self.levels[1] = ('1.txt', 15, 10)
        self.levels[2] = ('2.txt', 15, 10)
        self.levels[3] = ('little_test.txt', 3, 3)
        self.__level()

    def __level(self):
        lvl = QMessageBox()
        lvl.setWindowTitle('Select level')
        qbg = QButtonGroup(lvl)
        for i in range(1, 4):
            qbg.addButton(QCheckBox(str(i), lvl))
            qbg.buttons()[i - 1].move(10, 20 * (i - 1))
        qbg.buttons()[0].setCheckState(2)
        lvl.setStyleSheet('QLabel{min-width: 50px;' + 'min-height: {}px;'.format(str(len(qbg.buttons()) * 20)) + '}')
        lvl.setStandardButtons(QMessageBox.Ok)

        lvl.exec()

        for i in qbg.buttons():
            if i.checkState() == 2:
                numb = i.text()
                self.current = self.levels[int(numb)]

    def start(self):
        self.field = Field(self.current[1], self.current[2])
        self.field.load_data(os.path.join(os.path.dirname(__file__), 'levels', self.current[0]))
        self.__window_show()

    def __window_show(self):
        self.window = GameWindow()
        pr = Presenter(self.field, self.window)
        self.window.presenter = pr
        self.window.show()
