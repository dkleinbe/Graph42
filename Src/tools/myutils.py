
__author__ = 'dkleinbe'

try:
    from PyQt5.QtCore import QFile, QObject, pyqtSignal, QUrl, QResource, QTextStream
except ImportError:
    from PyQt4.QtCore import QFile, QObject, QResource, QTextStream

def ReadResourceTextFile(resFile):

    res = QResource(resFile)
    file = QFile(res.absoluteFilePath())
    file.open(QFile.ReadOnly | QFile.Text)
    textStream = QTextStream(file)
    data = textStream.readAll()
    file.close()

    return data