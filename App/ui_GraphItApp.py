# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphItApp.ui'
#
# Created: Tue Oct  7 23:53:51 2014
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindowUi(object):
    def setupUi(self, MainWindowUi):
        MainWindowUi.setObjectName(_fromUtf8("MainWindowUi"))
        MainWindowUi.resize(1015, 531)
        self.centralwidget = QtGui.QWidget(MainWindowUi)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.webViewGraph = QtWebKit.QWebView(self.centralwidget)
        self.webViewGraph.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webViewGraph.setObjectName(_fromUtf8("webViewGraph"))
        self.gridLayout.addWidget(self.webViewGraph, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindowUi.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindowUi)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1015, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindowUi.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindowUi)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindowUi.setStatusBar(self.statusbar)
        self.docWidgetLog = QtGui.QDockWidget(MainWindowUi)
        self.docWidgetLog.setObjectName(_fromUtf8("docWidgetLog"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.textEditLog = QtGui.QTextEdit(self.dockWidgetContents_2)
        self.textEditLog.setReadOnly(True)
        self.textEditLog.setObjectName(_fromUtf8("textEditLog"))
        self.gridLayout_3.addWidget(self.textEditLog, 0, 0, 1, 1)
        self.docWidgetLog.setWidget(self.dockWidgetContents_2)
        MainWindowUi.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.docWidgetLog)
        self.toolBar = QtGui.QToolBar(MainWindowUi)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindowUi.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionExit = QtGui.QAction(MainWindowUi)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/GraphIt/Resources/icon_quit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionConnect = QtGui.QAction(MainWindowUi)
        self.actionConnect.setObjectName(_fromUtf8("actionConnect"))
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionConnect)
        self.toolBar.addAction(self.actionExit)

        self.retranslateUi(MainWindowUi)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindowUi.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindowUi)

    def retranslateUi(self, MainWindowUi):
        MainWindowUi.setWindowTitle(_translate("MainWindowUi", "MainWindow", None))
        self.menuFile.setTitle(_translate("MainWindowUi", "File", None))
        self.docWidgetLog.setWindowTitle(_translate("MainWindowUi", "Log window éàë", None))
        self.toolBar.setWindowTitle(_translate("MainWindowUi", "toolBar", None))
        self.actionExit.setText(_translate("MainWindowUi", "Exit", None))
        self.actionConnect.setText(_translate("MainWindowUi", "Connect", None))
        self.actionConnect.setToolTip(_translate("MainWindowUi", "Connect", None))

from PyQt4 import QtWebKit
import GraphIt_rc
