__author__ = 'T0005632'

import unittest
import logging

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox
from PyQt5.QtCore import QFile

from ui_GraphItApp import Ui_MainWindowUi



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindowUi()
        self.ui.setupUi(self)

        file = QFile()

#        self.ui.exitAction.triggered.connect(QApplication.instance().quit)
#        self.ui.aboutQtAction.triggered.connect(QApplication.instance().aboutQt)




if __name__ == '__main__':

    import sys

    logging.basicConfig(level=logging.INFO) # filename='example.log',
    logging.info("Starting application")
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())