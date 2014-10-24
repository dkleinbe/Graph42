__author__ = 'T0005632'

import unittest
import logging
import sys
import html

try:
    from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox
    from PyQt5.QtCore import QFile, QObject, pyqtSignal
except ImportError:
    from PyQt4.QtGui import QApplication, QLabel, QMainWindow, QMessageBox

from tools.logstream import StreamRedirector
from tools.htmlcolorlog import HtmlColoredFormatter

from py2neo import neo4j

from ui_GraphItApp import Ui_MainWindowUi


logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindowUi()
        self.ui.setupUi(self)


        # create connections
#        self.ui.exitAction.triggered.connect(QApplication.instance().quit)
#        self.ui.aboutQtAction.triggered.connect(QApplication.instance().aboutQt)


        #self.ui.textEditLog.setTextFormat()
        formatter = HtmlColoredFormatter(
                                        '{asctime:<20}|{name:.<10}|{log_color}{levelname:.<10}{reset}| {message}{br}',
                                        style='{',
                                        #"%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
                                        datefmt=None,
                                        reset=True,
                                        log_colors={
                                                    'DEBUG': 'cyan',
                                                    'INFO': 'black',
                                                    'WARNING': 'orange',
                                                    'ERROR': 'red',
                                                    'CRITICAL': 'red',
                                                    }
                                    )
        logStream = StreamRedirector()
        logStream.messageWritten.connect(self.ui.textEditLog.insertHtml ) #insertPlainText

        ch = logging.StreamHandler(logStream)

        # create formatter and add it to the handlers
        #formatter = logging.Formatter('{asctime:<20}|{name:.<10}|{levelname:.<10}|{message}', style='{')
        ch.setFormatter(formatter)

        logger.addHandler(ch)

        logger.debug('Debug message')
        logger.info('Log window init <strong>done</strong>')
        logger.warning('Warning message')
        logger.error('Error message')
        logger.critical('Critical message')

        self.ui.actionConnect.triggered.connect(self.Neo4jConnect)


    def Neo4jConnect(self):

        try:
            db = "http://localhost:7474/db/data/"
            graph_db = neo4j.GraphDatabaseService(db)
            logger.info('neo4j version: %s', graph_db.neo4j_version)
        except:
            logger.error("Neo4j connection to %s - Unexpected error: %s", db, sys.exc_info()[1])

if __name__ == '__main__':


    logging.basicConfig(level=logging.DEBUG, format='{asctime:<20}|{name:.<10}|{levelname:.<10}| {message}', style='{')

    logger.info("Starting application")
    app = QApplication(sys.argv)
    logger.info("Application running")

    window = MainWindow()
    window.show()
    window.raise_()

    sys.exit(app.exec_())