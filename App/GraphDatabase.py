__author__ = 'dkleinbe'

import logging
import sys

from py2neo import neo4j, Node

logger = logging.getLogger("Graph42") # __main__
logger.addHandler(logging.NullHandler())

class GraphDatabase:

    def __init__(self):
        pass

    def Connect(self):
        try:
            db = "http://localhost:7474/db/data/"
            self. graph_db = neo4j.Graph(db)
            logger.info('neo4j version: %s', self.graph_db.neo4j_version)
        except neo4j.http.SocketError:
            logger.error("Neo4j connection to %s - Unexpected error: %s", db, sys.exc_info()[1].__class__.__name__)

    def node(self, node_id):

        rel_types = self.graph_db.relationship_types
        node = self.graph_db.node(node_id)

        return GraphNode(node)


class GraphNode:

    def __init__(self, node):

        self.node = node

    def labels(self):
        return self.node.labels

    def degree(self):
        """
        :return: number of relations
        """
        return self.node.degree

    def properties(self, name):
        """
        :param name: property name
        :return: property value
        """
        return self.node.properties[name]

    def relationships(self):
        """
        :return: relationships iterator
        """
        for rel in self.node.match():
            i_rel = GraphRelation(rel)
            yield i_rel


class GraphRelation:

    def __init__(self, relation):

        self.relation = relation

    def type(self):
        return self.relation.type

    def start_node(self):
        return GraphNode(self.relation.start_node)

    def end_node(self):
        return GraphNode(self.relation.end_node)


