import sys

from PyQt5.QtWidgets import QApplication

from src.game.gamemanager import Game

app = QApplication(sys.argv)

g = Game()
g.start()

sys.exit(app.exec_())
