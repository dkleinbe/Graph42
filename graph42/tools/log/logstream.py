__author__ = 'T0005632'

from logging import Handler
try:
    from PyQt5.QtCore import (QCoreApplication, \
                              QObject,\
                              pyqtSignal)
except ImportError:
    from PyQt4.QtCore import (QCoreApplication , \
                              QObject,\
                             pyqtSignal)

class StreamRedirector(QObject):

    messageWritten = pyqtSignal(str)

    def __init__(self, stream=None):
        QObject.__init__(self)

    def flush(self):
        self.messageWritten.emit('<br>')

    def fileno(self):
        return -1

    def write(self, msg):
        #self._textEdit.insertPlainText(msg)
        if not self.signalsBlocked():
            self.messageWritten.emit(msg)


class TextEditHtmlHandler(Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to a QTextEdit widget.
    """

    terminator = '<br>'

    def __init__(self, text_edit):
        """
        Initialize the handler.

        """
        Handler.__init__(self)

        self.text_edit = text_edit

    def flush(self):
        """
        Flushes the stream.
        """
        pass

    def emit(self, record):
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        try:
            msg = self.format(record)
            text_edit = self.text_edit

            text_edit.insertHtml(msg)
            text_edit.insertHtml(self.terminator)
            text_edit.ensureCursorVisible()  # Auto scroll TODO: set this as an option
            # force application to process event to display text synchronously
            QCoreApplication.processEvents()
        except Exception:
            self.handleError(record)
