__author__ = 'T0005632'

import logging
import sys


try:
    from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox, QPushButton
    from PyQt5.QtCore import QFile, QObject, pyqtSignal, QUrl, QResource, QTextStream

except ImportError:
    from PyQt4.QtGui import QApplication, QLabel, QMainWindow, QMessageBox, QPushButton
    from PyQt4.QtCore import QFile, QObject, QResource, QTextStream

from graph42.tools.log.logstream import TextEditHtmlHandler
from graph42.tools.log.htmlcolorlog import HtmlColoredFormatter
from graph42.tools.myutils import ReadResourceTextFile, ReadTextFile
from graph42.tools.scxml import QScxml

from graph42.ui.flowlayout import FlowLayout
from graph42.graphics.D3Graph import D3Graph, Js2PyBridge

from graph42.ui.ui_GraphItApp import Ui_MainWindowUi

from graph42.app.GraphDatabase import GraphDatabase,GraphNode, GraphRelation


logger = logging.getLogger("Graph42") # __name__


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindowUi()
        self.ui.setupUi(self)

        self.relTypesFlowLayout = FlowLayout(self.ui.groupRelTypes)
        self.labelFlowLayout = FlowLayout(self.ui.groupNodeLabels)

        self.ui.groupNodeLabels.setLayout(self.labelFlowLayout)

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
        # Establish Qt connections
        #
        #self.ui.actionConnect.triggered.connect(self.Neo4jConnect)

        #
        # Read resource files
        #
        useResource = False
        if (useResource):
            d3 = ReadResourceTextFile(":/GraphIt/Resources/d3.min.js")
            d3Test = ReadResourceTextFile(":/GraphIt/Resources/d3.test.js")
            body = ReadResourceTextFile(":/GraphIt/Resources/d3body.html")
        else:
            d3 = ReadTextFile("../ui/Resources/d3.min.js")
            d3Test = ReadTextFile("../ui/Resources/d3.test.js")
            body = ReadTextFile("../ui/Resources/d3body.html")

        #
        # set html frame content
        #
        self.ui.webViewGraph.page().mainFrame().setHtml(body)
        self.ui.webViewGraph.page().mainFrame().evaluateJavaScript(d3)
        self.ui.webViewGraph.page().mainFrame().evaluateJavaScript(d3Test)

        self.js2py = Js2PyBridge()
        self.ui.webViewGraph.page().mainFrame().addToJavaScriptWindowObject('js2py', self.js2py)
        self.js2py.register_event_handler('node_selected', self.node_selected)
        #
        # Init state machine
        #
        self.state_machine = QScxml()
        self.state_machine.registerObject(self.ui, "ui")
        self.state_machine.registerObject(self, "g42")
        self.state_machine.load("../ui/Resources/Graph42.scxml")
        self.state_machine.start()

    def node_selected(self, evt):

        logger.info("node selected: [%s]", evt['node_id'])

    def Neo4jConnect(self):

        self.graphDB = GraphDatabase()

        logger.info("Connecting to database")
        try:
            self.graphDB.connect()
        except:
            return False

        return True

    def InitGraphGui(self):
        #
        # Add label buttons
        #
        for label in self.graphDB.node_labels_set():
            self.labelFlowLayout.addWidget(QPushButton(label))
        #
        # Add relation buttons
        #
        for rel in self.graphDB.relationship_types():
            self.relTypesFlowLayout.addWidget(QPushButton(rel))

        if 0:
            node = self.graphDB.node(1)
            logger.info("node: %s", node)
            logger.info("node degree: %s", node.degree())

            props = node.properties()

            for propName, propValue in props.items():
                logger.info("prop : %s %s", propName, propValue )
            for rel in node.relationships():
                labels = rel.end_node().labels()
                for label in labels:
                    logger.info("labels : %s", label)
                logger.info("relation: %s <-%s-> %s %s",
                            rel.start_node().property("name"),
                            rel.type(),
                            label,
                            rel.end_node().property("title"))

        self.GraphTest()

        return True

    def GraphTest(self):

        logger.info("TestGraph begin")

        #rec_list = self.graphDB.execute_cypher("MATCH (n:`Movie`) RETURN n LIMIT 25")
        rec_list = self.graphDB.execute_cypher("MATCH (a)-[r]-(b) RETURN a,r,b LIMIT 20")

        d3graph = D3Graph(self.ui.webViewGraph.page().mainFrame())

        sub_graph = rec_list.to_subgraph()
        for node in sub_graph.nodes:
            gnode = GraphNode(node)
            d3graph.add_node(gnode)
        for rel in sub_graph.relationships:
            grel = GraphRelation(rel)
            d3graph.add_link(grel.start_node(), grel.end_node(), grel.type())

        d3graph.restart()

        logger.info("TestGraph end")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='{asctime:<20}|{levelname:.<8}|{name:}|{filename}:{lineno}| {message}',
                        style='{')

    logger.info("Starting application")
    app = QApplication(sys.argv)
    logger.info("Application running")

    window = MainWindow()
    window.show()
    window.raise_()

    sys.exit(app.exec_())