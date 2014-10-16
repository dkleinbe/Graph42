__author__ = 'T0005632'


from PyQt5.QtCore import (QObject,\
                          pyqtSignal)

class StreamRedirector(QObject):

    messageWritten = pyqtSignal(str)

    def flush(self):
        pass
    def fileno(self):
        return -1
    def write(self, msg):
        #self._textEdit.insertPlainText(msg)
        if ( not self.signalsBlocked() ):
            self.messageWritten.emit(msg)