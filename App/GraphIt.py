__author__ = 'T0005632'

import unittest
import logging
import sys

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox

from PyQt5.QtCore import (QFile, \
                          QObject,\
                          pyqtSignal)

from ui_GraphItApp import Ui_MainWindowUi


logger = logging.getLogger(__name__)

class XStream(QObject):
    _stdout = None
    _stderr = None

    messageWritten = pyqtSignal(str)

    def flush( self ):
        pass

    def fileno( self ):
        return -1

    def write( self, msg ):
        if ( not self.signalsBlocked() ):
            self.messageWritten.emit(msg)

    @staticmethod
    def stdout():
        if ( not XStream._stdout ):
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if ( not XStream._stderr ):
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindowUi()
        self.ui.setupUi(self)

        file = QFile()

#        self.ui.exitAction.triggered.connect(QApplication.instance().quit)
#        self.ui.aboutQtAction.triggered.connect(QApplication.instance().aboutQt)
                # create connections
        XStream.stdout().messageWritten.connect( self.ui.textEditLog.insertPlainText ) # insertHtml
        XStream.stderr().messageWritten.connect( self.ui.textEditLog.insertPlainText ) # insertPlainText

        self.ui.actionConnect.triggered.connect(self.test)
        #self.ui.textEditLog.setTextFormat()

    def test( self ):
        # print some stuff
        print ('<b>testing</b>')
        print ('testing2')

        # log some stuff
        logger.debug('Testing debug')
        logger.info('Testing info')
        logger.warning('Testing warning')
        logger.warning('Testing <b>warning</b>')
        logger.error('Testing error')

        # error out something
        #print (blah)

if __name__ == '__main__':


    logging.basicConfig(level=logging.INFO)

    logger.info("Starting application")
    app = QApplication(sys.argv)
    logger.info("Application running")

    ch = logging.StreamHandler(XStream.stderr())
    # create formatter and add it to the handlers
    #formatter = logging.Formatter('%(asctime){:<10} - %(name){:<10} - %(levelname){:<10} - %(message){:<10}', style='{')
    formatter = logging.Formatter('{asctime:<20}|{name:.<10}|{levelname:.<10}|{message}', style='{')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())