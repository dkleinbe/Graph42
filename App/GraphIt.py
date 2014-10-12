__author__ = 'T0005632'

import unittest
import logging
import sys

from tools.logstream import StreamRedirector

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox

from PyQt5.QtCore import (QFile, \
                          QObject,\
                          pyqtSignal)

from ui_GraphItApp import Ui_MainWindowUi


logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindowUi()
        self.ui.setupUi(self)

        file = QFile()

        # create connections
#        self.ui.exitAction.triggered.connect(QApplication.instance().quit)
#        self.ui.aboutQtAction.triggered.connect(QApplication.instance().aboutQt)


        #self.ui.textEditLog.setTextFormat()

        logStream = StreamRedirector()
        logStream.messageWritten.connect(self.ui.textEditLog.insertHtml ) #insertPlainText
        ch = logging.StreamHandler(logStream)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('{asctime:<20}|{name:.<10}|{levelname:.<10}|{message}', style='{')
        ch.setFormatter(formatter)

        logger.addHandler(ch)
        logger.info('Log window init <u>done</u>')


if __name__ == '__main__':


    logging.basicConfig(level=logging.INFO)

    logger.info("Starting application")
    app = QApplication(sys.argv)
    logger.info("Application running")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())