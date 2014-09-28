# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphItApp.ui'
#
# Created: Sun Sep 28 19:33:22 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindowUi(object):
    def setupUi(self, MainWindowUi):
        MainWindowUi.setObjectName("MainWindowUi")
        MainWindowUi.resize(1015, 531)
        self.centralwidget = QtWidgets.QWidget(MainWindowUi)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.webViewGraph = QtWebKitWidgets.QWebView(self.centralwidget)
        self.webViewGraph.setUrl(QtCore.QUrl("about:blank"))
        self.webViewGraph.setObjectName("webViewGraph")
        self.gridLayout.addWidget(self.webViewGraph, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindowUi.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowUi)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1015, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindowUi.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowUi)
        self.statusbar.setObjectName("statusbar")
        MainWindowUi.setStatusBar(self.statusbar)
        self.docWidgetLog = QtWidgets.QDockWidget(MainWindowUi)
        self.docWidgetLog.setObjectName("docWidgetLog")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textEditLog = QtWidgets.QTextEdit(self.dockWidgetContents_2)
        self.textEditLog.setReadOnly(True)
        self.textEditLog.setObjectName("textEditLog")
        self.gridLayout_3.addWidget(self.textEditLog, 0, 0, 1, 1)
        self.docWidgetLog.setWidget(self.dockWidgetContents_2)
        MainWindowUi.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.docWidgetLog)
        self.toolBar = QtWidgets.QToolBar(MainWindowUi)
        self.toolBar.setObjectName("toolBar")
        MainWindowUi.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionExit = QtWidgets.QAction(MainWindowUi)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/GraphIt/Resources/icon_quit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon)
        self.actionExit.setObjectName("actionExit")
        self.actionConnect = QtWidgets.QAction(MainWindowUi)
        self.actionConnect.setObjectName("actionConnect")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionConnect)
        self.toolBar.addAction(self.actionExit)

        self.retranslateUi(MainWindowUi)
        self.actionExit.triggered.connect(MainWindowUi.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindowUi)

    def retranslateUi(self, MainWindowUi):
        _translate = QtCore.QCoreApplication.translate
        MainWindowUi.setWindowTitle(_translate("MainWindowUi", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindowUi", "File"))
        self.docWidgetLog.setWindowTitle(_translate("MainWindowUi", "Log window éàë"))
        self.toolBar.setWindowTitle(_translate("MainWindowUi", "toolBar"))
        self.actionExit.setText(_translate("MainWindowUi", "Exit"))
        self.actionConnect.setText(_translate("MainWindowUi", "Connect"))
        self.actionConnect.setToolTip(_translate("MainWindowUi", "Connect"))

from PyQt5 import QtWebKitWidgets
import GraphIt_rc
