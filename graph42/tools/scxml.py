__author__ = 'T0005632'

import logging

try:
    from PyQt5.QtCore import QFile, QStateMachine, QState, QHistoryState, QFinalState, QAbstractTransition, QXmlStreamReader, QIODevice
except ImportError:
    from PyQt4.QtCore import QFile, QStateMachine, QState, QHistoryState, QFinalState, QAbstractTransition, QXmlStreamReader, QIODevice

logger = logging.getLogger("Graph42")  # __main__
#logger.addHandler(logging.NullHandler())

class QScxml(QStateMachine):

    def __init__(self):

        super(QScxml, self).__init__()

    @staticmethod
    def load(filename):


        l = ScxmlLoader()
        file = QFile(filename)
        if not file.open(QFile.ReadOnly):
            logger.error("Error while opening file: <%s>", filename)
            return False
        logger.info("Loading file: <%s> ", filename)
        return l.load(file)


class QScxmlTransition(QAbstractTransition):

    def __init__(self, state, machine):

        super(QAbstractTransition, self).__init__(state)

        self.scxml = machine
        self.prog = ""

    def setConditionExpression(self, cond):
        self.prog = cond

    def setEventPrefixes(self,ev):
        self.ev = ev

class ScExecContext:

    Unknown = 0
    StateEntry = 1
    StateExit = 2
    Transition = 3

    def __init__(self):
        self.type = self.Unknown
        self.script = ""

class ScHistoryInfo:
    pass



class ScxmlLoader:

    def __init__(self):

        self.stateMachine = None
        self.stateInfo = dict()
        self.statesWithFinal = set()
        self.historyInfo = list()


    def load(self, dev):

        self.stateMachine = QScxml()
        self.loadState(dev, self.stateMachine)


    def loadState(self, dev, stateParam, stateID = ""):

        stateByID = dict()
        curExecContext = ScExecContext()
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
                    logger.info("Element :<%s>", r.name())
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
                        logger.info("Creating state")
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
                                self.stateMachine.setInitialState(newState)
                            else:
                                curState.setInitialState(newState)
                        #
                        # TODO implement src attribute management in state element
                        #
                        initialID = r.attributes().value("initial")
                        stateByID[id] = newState
                        curState = newState
                        curExecContext.state = newState
                #
                # <initial>
                #
                elif name == "initial":
                    if curState is not None and self.stateInfo[curState] == "":
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
                        stateByID[id] = curHistoryState
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
                        stateByID[id] = f
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
                    # TODO Format log string
                    curExecContext.script += "logger.info(...)"
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
                        inf = ScHistoryInfo()
                        inf.targets = r.attributes().value("target") # TODO split targets
                        curExecContext.type = ScExecContext.Transition
                        curExecContext.script = ""
                        curTransition = QScxmlTransition(curState, self.stateMachine)
                        curTransition.setConditionExpression(r.attributes().value("cond"))
                        curTransition.setEventPrefixes(r.attributes().value("event").split(' '))










if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG,
                        format='{asctime:<20}|{levelname:.<8}|{name:}|{filename}:{lineno}| {message}',
                        style='{')
    scxml_machine = QScxml()

    scxml_machine = QScxml.load("ExifMediaRename.scxml", )


