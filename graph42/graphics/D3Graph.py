__author__ = 'T0005632'

import logging
import sys

try:
    from PyQt5 import QtCore, QtGui, QtWebKit
    from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox, QWidget
    from PyQt5.QtCore import pyqtSlot
except ImportError:
    from PyQt4 import QtCore, QtGui, QtWebKit


logger = logging.getLogger("Graph42")  # __main__
logger.addHandler(logging.NullHandler())

class Js2PyBridge(QWidget):
    """ A class to bridge Javascript world and PyQt world
    """
    @pyqtSlot(str)
    def showMessage(self, msg):
        """Open a message box and display the specified message."""
        msgBox = QMessageBox()
        msgBox.setText(msg)
        #msgBox.setInformativeText("Do you want to save your changes?")
        #msgBox.setStandardButtons(QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel);
        #msgBox.setDefaultButton(QMessageBox::Save);
        ret = msgBox.exec();

    @pyqtSlot(int)
    def node_selected(self, d3_id):
        """
        :param d3_id: node id in d3.js world
        :return:
        """
        msgBox = QMessageBox()
        msgBox.setText(str(d3_id))
        ret = msgBox.exec();

    def _pyVersion(self):
        """Return the Python version."""
        return sys.version

    """Python interpreter version property."""
    pyVersion = QtCore.pyqtProperty(str, fget=_pyVersion)

class D3Graph:

    __nodes = dict()
    __links = dict()
    __labels = dict()

    def __init__(self, frame):
        self.frame = frame

    def add_link(self, start, end, link_type):
        """ Add link to D3 graph

        Link is added only if it does not exist yet

        :param start:
        :param end:
        :param link_type:
        :return:
        """

        key = str(start.id()) + "_" + link_type + "_" + str(end.id())

        # Add link only if it does not exist yet
        if (key in self.__links):
            return

        js = "links.push({source: " + self.__nodes[start.id()] + ", target: " + self.__nodes[end.id()] + "});"

        d3_link_id = self.frame.evaluateJavaScript(js) - 1

        self.__links[key] = d3_link_id

    def add_node(self, node):
        """ Add a node to D3 graph

        Node is added only if it does not exist yet

        :param node: node to add
        :return: None
        """

        # Add node only if it does not exist yet
        if node.id() in self.__nodes:
            return

        labels = node.labels()
        for label in labels:
                break

        if label not in self.__labels:
            self.__labels[label] = len(self.__labels)

        js = "nodes.push({index: " + str(node.id()) + ", " +\
                        "name: \"" + str(node.id()) + "\", " +\
                        "group: " + str(self.__labels[label]) + \
                            " });"

        d3_node_id = self.frame.evaluateJavaScript(js) - 1
        self.__nodes[node.id()] = str(d3_node_id)
        logger.info("node id %s - > d3 id: %s", node.id(), d3_node_id)

    def restart(self):
        """ Restart rendering
        :return:
        """
        self.frame.evaluateJavaScript("restart();")