__author__ = 'T0005632'

import logging
import sys


try:
    from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox
    from PyQt5.QtCore import QFile, QObject, pyqtSignal, QUrl, QResource, QTextStream

except ImportError:
    from PyQt4.QtGui import QApplication, QLabel, QMainWindow, QMessageBox
    from PyQt4.QtCore import QFile, QObject, QResource, QTextStream

from Src.tools.log.logstream import TextEditHtmlHandler
from Src.tools.log.htmlcolorlog import HtmlColoredFormatter
from Src.tools.myutils import ReadResourceTextFile

from ui_GraphItApp import Ui_MainWindowUi

from GraphDatabase import GraphDatabase


logger = logging.getLogger("Graph42") # __name__

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindowUi()
        self.ui.setupUi(self)


        # create connections
#        self.ui.exitAction.triggered.connect(QApplication.instance().quit)
#        self.ui.aboutQtAction.triggered.connect(QApplication.instance().aboutQt)


        # create formatter
        formatter = HtmlColoredFormatter(
                                        '{asctime:<20}|{log_color}{levelname:.<8}{reset}|{name:}|{filename}:{lineno}| {message}',
                                        style='{',
                                        datefmt=None,
                                        reset=True,
                                        log_colors={
                                                    'DEBUG': 'blue',
                                                    'INFO': 'black',
                                                    'WARNING': 'orange',
                                                    'ERROR': 'red',
                                                    'CRITICAL': 'red',
                                                    }
                                    )

        #create QTextEdit html handler
        logHtmlHandler = TextEditHtmlHandler(self.ui.textEditLog)
        # add formatter to the handlers
        logHtmlHandler.setFormatter(formatter)
        # add handler to top level logger
        #logging.getLogger().addHandler(logHtmlHandler)
        logger.addHandler(logHtmlHandler)


        if (0):
            logger.debug('Debug message')
            logger.info('Log window init <strong>done</strong>')
            logger.warning('Warning message')
            logger.error('Error message')
            logger.critical('Critical message')

        #
        # Establish connections
        #
        self.ui.actionConnect.triggered.connect(self.Neo4jConnect)


        self.ui.webViewGraph.page().mainFrame().setHtml("\
<style>\
rect {\
  fill: none;\
  pointer-events: all;\
}\
.node {\
  fill: #F00;\
}\
.cursor {\
  fill: none;\
  stroke: brown;\
  pointer-events: none;\
}\
.link {\
  stroke: #999;\
}\
</style>")


        d3 = ReadResourceTextFile(":/GraphIt/Resources/d3.min.js")
        self.ui.webViewGraph.page().mainFrame().evaluateJavaScript(d3)

        useResource = False
        if (useResource):
            d3Test = ReadResourceTextFile(":/GraphIt/Resources/d3.test.js")
        else:
            file = QFile("./Resources/d3.test.js")
            file.open(QFile.ReadOnly | QFile.Text)
            textStream = QTextStream(file)
            d3Test = textStream.readAll()
            file.close()

        self.ui.webViewGraph.page().mainFrame().evaluateJavaScript(d3Test)

    def Neo4jConnect(self):



        graphDB = GraphDatabase()

        graphDB.connect()

        node = graphDB.node(1)
        logger.info("node: %s", node)
        logger.info("node degree: %s", node.degree())

        props = node.properties()

        for propName, propValue in props.items():
            logger.info("prop : %s %s", propName, propValue )
        for rel in node.relationships():
            labels = rel.end_node().labels()
            for label in labels:
                logger.info("labels : %s", label)
            logger.info("relation: %s <-%s-> %s",
                        rel.start_node().property("name"),
                        rel.type(),
                        label)

        self.ui.webViewGraph.page().mainFrame().evaluateJavaScript("nodes.push({x: 10, y: 10});")

        self.GraphTest()

    def GraphTest(self):

        logger.info("TestGraph begin")


        aze = "var graph = Viva.Graph.graph(); graph.addLink(1, 2); graph.addLink(1, 3); graph.addLink(2, 3); var renderer = Viva.Graph.View.renderer(graph); renderer.run(); alert(6)"
        aze = "node = {x: 50, y: 50},n = nodes.push(node), links.push({source: nodes[1], target: nodes[0]});"
        aze = "links.push({source: nodes[0], target: nodes[1]}); restart();"
        self.ui.webViewGraph.page().mainFrame().evaluateJavaScript(aze);

        logger.info("TestGraph end")

if __name__ == '__main__':


    logging.basicConfig(level=logging.DEBUG, format='{asctime:<20}|{levelname:.<8}|{name:}|{filename}:{lineno}| {message}', style='{')

    logger.info("Starting application")
    app = QApplication(sys.argv)
    logger.info("Application running")

    window = MainWindow()
    window.show()
    window.raise_()

    sys.exit(app.exec_())