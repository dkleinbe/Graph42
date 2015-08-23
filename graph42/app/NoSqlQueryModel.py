__author__ = 'chris'

import logging
from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt
from py2neo import Service, Resource, Node, Rel, Relationship, Subgraph, Path, Finished

class NoSqlQueryModel(QAbstractTableModel):

    def __init__(self):

        super(NoSqlQueryModel, self).__init__()
        self.graph_db = None
        self.record_list = None
        self.row_count = 0
        self.column_count = 0

    def setCypher(self, stmt, db):

        self.record_list = db.execute_cypher(stmt)
        self.row_count = len(self.record_list.records)
        self.column_count = len(self.record_list.columns)
        pass

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):

        return self.row_count

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):

        return self.column_count

    def data(self, QModelIndex, int_role=None):

        if not QModelIndex.isValid():
            return QVariant()

        if QModelIndex.row() > self.row_count:
            return QVariant()

        if QModelIndex.column() > self.column_count:
            return QVariant()

        if int_role == Qt.DisplayRole:
            row = QModelIndex.row()
            col = QModelIndex.column()
            if isinstance(self.record_list.records[row][col], Node):
                node = self.record_list.records[row][col]
                ret_str = ''
                for label in node.labels:
                    ret_str += str(label)

                return ret_str
            if isinstance(self.record_list.records[row][col], Relationship):
                return "Relationship"
            return 'Unknown'

    def headerData(self, p_int, Qt_Orientation, role=None):

        if role != Qt.DisplayRole:
            return QVariant()

        if Qt_Orientation == Qt.Horizontal:
            return "Column " + str(p_int)
        else:
            return str(p_int)


