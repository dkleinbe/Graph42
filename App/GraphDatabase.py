__author__ = 'dkleinbe'

import logging
import sys

from py2neo import neo4j, Node

logger = logging.getLogger(__name__)

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

    def GetNode(self, node_id):

        rel_types = self.graph_db.relationship_types
        node = self.graph_db.node(node_id)

        logger.info("Relations type: %s", rel_types)
        logger.info("node: %s", node)

        return node
