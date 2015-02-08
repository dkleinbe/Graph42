__author__ = 'T0005632'

import logging
import sys

try:
    from PyQt5.QtCore import QObject, QFile, QStateMachine, QState, QHistoryState, QFinalState, QAbstractTransition, \
        QXmlStreamReader, QIODevice, pyqtSignal, pyqtSlot
    from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
except ImportError:
    from PyQt4.QtCore import QObject, QFile, QStateMachine, QState, QHistoryState, QFinalState, QAbstractTransition, \
        QXmlStreamReader, QIODevice

logger = logging.getLogger("Graph42")  # __main__
#logger.addHandler(logging.NullHandler())

class QScxml(QStateMachine):

    def __init__(self):

        super(QScxml, self).__init__()
        self.knownEvents = set()
        self.execContexts = list()

    @staticmethod
    def load(filename):


        l = ScxmlLoader()
        file = QFile(filename)
        if not file.open(QFile.ReadOnly):
            logger.error("Error while opening file: <%s>", filename)
            return False
        logger.info("Loading file: <%s> ", filename)
        return l.load(file)

    def addExecContext(self,execCtx):
        self.execContexts.append(execCtx)

    @pyqtSlot()
    def handleStateFinished(self):

        state = self.sender()
        if state:
            pass
            # self.postEvent(QEvent()) # TODO send relevant event

class QScxmlTransition(QAbstractTransition):

    def __init__(self, state, machine):

        super(QAbstractTransition, self).__init__(state)

        self.scxml = machine
        self.prog = ""

    def setConditionExpression(self, cond):
        self.prog = cond

    def setEventPrefixes(self,ev):
        self.ev = ev

    def eventPrefixes(self):
        return self.ev

    def eventTest(self, QEvent):
        return True

    def onTransition(self, QEvent):
        pass


class QScxmlScriptExec(QObject):

    def __init__(self, src, scx):

        super(QScxmlScriptExec, self).__init__()

        self.src = src
        self.scxml = scx

    @pyqtSlot()
    def exec(self):
        exec(self.src)
        #self.scxml.executeScript(self.src)


class ScExecContext:

    Unknown = 0
    StateEntry = 1
    StateExit = 2
    Transition = 3

    def __init__(self):
        self.type = self.Unknown
        self.script = str()
        self.state =None
        self.stateMachine = None

    def applyScript(self):

        execCtx = QScxmlScriptExec(self.script, self.stateMachine)
        self.stateMachine.addExecContext(execCtx)
        if len(self.script) != 0:
            if self.type == self.StateEntry:
                logger.info("Connecting [%s] entered", self.state.objectName())
                self.state.entered.connect(execCtx.exec)
            elif self.type == self.StateExit:
                logger.info("Connecting [%s] exited", self.state.objectName())
                self.state.exited.connect(execCtx.exec)
            elif self.type == self.Transition:
                logger.info("Connecting [%s] triggered", self.state.objectName())
                self.state.triggered.connect(execCtx.exec)

            pass

class ScHistoryInfo:
    pass

class ScTransitionInfo:
    pass

class ScxmlLoader:

    def __init__(self):

        self.stateMachine = None
        self.stateInfo = dict()
        self.statesWithFinal = set()
        self.historyInfo = list()
        self.stateByID = dict()
        self.transitions = list()
        self.signalEvents = list()


    def load(self, dev):

        self.stateMachine = QScxml()
        self.stateMachine.setObjectName("scxml")
        #
        # Traverse through the state
        #
        self.loadState(dev, self.stateMachine)
        #
        # resolve history state
        #
        for h in self.historyInfo:
            h.hstate.setDefaultState(self.stateByID[h.defaultStateID])
        #
        # TODO resolve signal events
        #

        #
        # resolve finish states connection
        #
        for s in self.statesWithFinal:
            s.finished.connect(self.stateMachine.handleStateFinished)
        #
        # resolve transitions
        #
        for t in self.transitions:
            states = list()
            if len(t.targets) != 0:
                for s in t.targets:
                    if len(s.strip()) != 0:
                        st = self.stateByID[s]
                        if st is not None:
                            states.append(st)
                t.transition.setTargetStates(states)

        return self.stateMachine


    def loadState(self, dev, stateParam, stateID = ""):

        curExecContext = ScExecContext()
        curExecContext.stateMachine = self.stateMachine
        curHistoryState = None

        r = QXmlStreamReader(dev)

        while not r.atEnd():
            r.readNext()
            if r.isStartElement():
                logger.info("Element :<%s>", r.name())
                #
                # <scxml>
                #
                name = r.name().lower()
                if name == "scxml":

                    if stateID == "":
                        topLevelState = curState = stateParam
                        self.stateInfo[curState] = r.attributes().value("initial")
                        if curState == self.stateMachine :
                            pass
                #
                # <state> || <parallel>
                #
                elif name == "state" or name == "parallel":
                    inRoot = False
                    id = r.attributes().value("id")
                    newState = None
                    #
                    # Create state
                    #
                    if curState is not None:
                        logger.info("Creating state [%s] child of [%s]", id, curState.objectName())
                        type = QState.ExclusiveStates if name == "state" else QState.ParallelStates
                        newState = QState(type, curState)
                    #
                    # ???
                    #
                    elif id == stateID :
                        topLevelState = newState = stateParam

                    if newState is not None:
                        self.stateInfo[newState] = r.attributes().value("initial")
                        newState.setObjectName(id)
                        #
                        # initial state
                        #
                        if id is not "" and self.stateInfo[curState] == id:
                            if curState == self.stateMachine:
                                logger.info("Setting [%s] initial state to [%s]",
                                            self.stateMachine.objectName(),
                                            newState.objectName())
                                self.stateMachine.setInitialState(newState)
                            else:
                                logger.info("Setting [%s] initial state to [%s]",
                                            curState.objectName(),
                                            newState.objectName())
                                curState.setInitialState(newState)
                        #
                        # TODO implement src attribute management in state element
                        #
                        initialID = r.attributes().value("initial")
                        self.stateByID[id] = newState
                        curState = newState
                        curExecContext.state = newState
                #
                # <initial>
                #
                elif name == "initial":
                    if curState is not None and self.stateInfo[curState] == "":
                        logger.info("Creating state [%s] child of [%s]", id, curState.objectName())
                        newState = QState(curState)
                        curState.setInitialState(newState)
                #
                # <history>
                #
                elif name == "history":
                    if curState is not None:
                        id = r.attributes().value("id")
                        type = r.attributes().value("type")
                        type = QHistoryState.ShallowHistory if type == "shallow" else QHistoryState.DeepHistory
                        curHistoryState = QHistoryState(type)
                        self.stateByID[id] = curHistoryState
                #
                # <final>
                #
                elif name == "final":
                    if curState is not None:
                        id = r.attributes().value("id")
                        f = QFinalState(curState)
                        f.setObjectName(id)
                        curExecContext.state = f
                        self.statesWithFinal.add(curState)
                        gp = curState.parentState()
                        if gp is not None:
                            if gp.childMode() == QState.ParallelStates:
                                self.statesWithFinal.add()
                        self.stateByID[id] = f
                #
                # <script>
                #
                elif name == "script":
                    txt = r.readElementText()
                    #
                    # The SCXML Processor MUST evaluate any <script> element that is a child
                    # of <scxml> at document load time
                    #
                    if curExecContext.type == ScExecContext.Unknown and curState == topLevelState:
                        # TODO execute script
                        pass
                    else:
                        curExecContext.script += txt
                #
                # <log>
                #
                elif name == "log":
                    curExecContext.script += 'logger.info("[' + \
                                             r.attributes().value("label") + '] [' +  \
                                             r.attributes().value("level") + '] ' + r.attributes().value("expr") + '")'



                #
                # <assign>
                #
                elif name == "assign":
                    pass
                #
                # <if>
                #
                elif name == "if":
                    pass
                #
                # <elseif>
                #
                elif name == "elseif":
                    pass
                #
                # <else>
                #
                elif name == "else":
                    pass
                #
                # <cancel>
                #
                elif name == "cancel":
                    pass
                #
                # <onentry>
                #
                elif name == "onentry":
                    curExecContext.type = ScExecContext.StateEntry
                    curExecContext.script = ""
                #
                # <onexit>
                #
                elif name == "onexit":
                    curExecContext.type = ScExecContext.StateExit
                    curExecContext.script = ""
                #
                # <raise>
                #
                elif name == "raise":
                    pass
                #
                # <send>
                #
                elif name == "send":
                    pass
                #
                # <invoke>
                #
                elif name == "invoke":
                    pass
                #
                # <transition>
                #
                elif name == "transition":
                    if curHistoryState is not None:
                        inf = ScHistoryInfo()
                        inf.hstate = curHistoryState
                        inf.defaultStateID = r.attributes().value("target")
                        self.historyInfo.append(inf)
                    else:
                        inf = ScTransitionInfo()
                        inf.targets = r.attributes().value("target").split() # TODO split targets
                        curExecContext.type = ScExecContext.Transition
                        curExecContext.script = ""
                        curTransition = QScxmlTransition(curState, self.stateMachine)
                        curTransition.setConditionExpression(r.attributes().value("cond"))
                        curTransition.setEventPrefixes(r.attributes().value("event").split(' '))
                        for pfx in curTransition.eventPrefixes():
                            if pfx is not "*":
                                self.stateMachine.knownEvents.add(pfx)
                        curExecContext.trans = curTransition
                        inf.transition = curTransition
                        self.transitions.append(inf)
                        for pfx in curTransition.eventPrefixes():
                            if pfx.startswith("q-signal:"):
                                self.signalEvents.append(pfx)
                        curTransition.setObjectName(curState.objectName()
                                                    + " to "
                                                    + ' '.join(curTransition.eventPrefixes()))

            #
            # End element
            #
            elif r.isEndElement():
                name = r.name().lower()
                #
                # </state> or </parallel>
                #
                if name == "state" or name == "parallel":
                    if curState == topLevelState:
                        return
                    else:
                        curState = curState.parent()
                        curExecContext.state = curState
                #
                # </history>
                #
                elif name == "history":
                    curHistoryState = None
                #
                # </final>
                #
                elif name == "final":
                    curExecContext.state = curExecContext.state.parentState()
                #
                # </if>
                #
                elif name == "if":
                    pass
                #
                # </send> </raise>
                #
                elif name == "send" or name == "raise":
                    pass
                #
                # </onentry> </onexit> </scxml>
                #
                elif name == "onentry" or name == "onexit" or name == "scxml":
                    curExecContext.state = curState
                    curExecContext.type = ScExecContext.StateExit if name == "onexit" else ScExecContext.StateEntry
                    curExecContext.applyScript()
                    curExecContext.type = ScExecContext.Unknown
                    curExecContext.script = ""
                #
                # </transition>
                #
                elif name == "transition":
                    if curHistoryState is None:
                        curExecContext.trans = curTransition
                        curExecContext.type = ScExecContext.Transition
                        curExecContext.applyScript()
                        curExecContext.script = ""
                    curExecContext.type = ScExecContext.Unknown

def toto():
    logger.info("AZEAZEEA")

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG,
                        format='{asctime:<20}|{levelname:.<8}|{name:}|{filename}:{lineno}| {message}',
                        style='{')
    scxml_machine = QScxml()

    scxml_machine = QScxml.load("test144.scxml", )



    app = QApplication(sys.argv)
    logger.info("Application running")

    window = QMainWindow()

    pb = QPushButton(window)
    window.show()
    window.raise_()

    scxml_machine.start()

    if 0:
        sm = QStateMachine()
        s1 = QState()
        s1.entered.connect(toto)
        sm.addState(s1)
        sm.setInitialState(s1)
        sm.start()

    sys.exit(app.exec_())
