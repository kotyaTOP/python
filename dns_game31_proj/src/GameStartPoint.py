import sys
from PyQt5.QtWidgets import QApplication

from src.start_dialog import StartWindow

app = QApplication(sys.argv)
ex = StartWindow()
sys.exit(app.exec_())
