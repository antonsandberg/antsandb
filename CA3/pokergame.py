""" Oliver Johansson and Anton Sandberg """
""" Computer Assignment 3 """
""" Group 7 """

from PyQt5.QtCore import *
import pokermodel_2
import PokerGrafiken
import sys
from PyQt5.QtWidgets import *

qt_app = QApplication(sys.argv)
game = pokermodel_2.TexasHoldemModel()
view = PokerGrafiken.PokerTable(game)
view.show()
sys.exit(qt_app.exec())