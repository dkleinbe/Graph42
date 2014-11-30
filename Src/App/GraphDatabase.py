__author__ = 'dkleinbe'

import logging
import sys

from py2neo import neo4j, Node

logger = logging.getLogger("Graph42") # __main__
logger.addHandler(logging.NullHandler())

class GraphDatabase:

    def __init__(self):
        pass

    def connect(self):
        try:
            db = "http://localhost:7474/db/data/"
            self.graph_db = neo4j.Graph(db)
            logger.info('neo4j version: %s', self.graph_db.neo4j_version)
        except :
            logger.error("Neo4j connection to %s - Unexpected error: %s", db, sys.exc_info()[1].__class__.__name__)

    def node(self, node_id):
        """
        :param node_id: node's Id
        :return: GraphNode
        """
        rel_types = self.graph_db.relationship_types
        node = self.graph_db.node(node_id)

        return GraphNode(node)


class GraphNode:

    def __init__(self, node):

        self.node = node

    def labels(self):
        """
        :return: labels set
        """
        return self.node.labels

    def degree(self):
        """
        :return: number of relations
        """
        return self.node.degree

    def property(self, key):
        """
        :param key: property name
        :return: property value
        """
        return self.node.properties[key]

    def properties(self):
        """
        :return: node's properties dict
        """
        return self.node.properties

    def relationships(self):
        """
        :return: node's relationships iterator
        """
        for rel in self.node.match():
            i_rel = GraphRelation(rel)
            yield i_rel


class GraphRelation:

    def __init__(self, relation):

        self.relation = relation

    def type(self):
        """
        :return: relation type
        """
        return self.relation.type

    def start_node(self):
        """
        :return: start :class:`.GraphNode` of the relation
        """
        return GraphNode(self.relation.start_node)

    def end_node(self):
        """
        :return: end GraphNode of the relation
        """
        return GraphNode(self.relation.end_node)


