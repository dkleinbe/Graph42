__author__ = 'T0005632'

import logging
import sys

logger = logging.getLogger("Graph42") # __main__
logger.addHandler(logging.NullHandler())

class D3Graph:

    __nodes = dict()
    __links = dict()

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
        if (node.id() in self.__nodes):
            return

        js = "nodes.push({index: " + \
                            str(node.id()) + \
                            ", name: \"" + \
                            str(node.id()) + \
                            "\" });"

        d3_node_id = self.frame.evaluateJavaScript(js) - 1
        self.__nodes[node.id()] = str(d3_node_id)
        logger.info("node id %s - > d3 id: %s", node.id(), d3_node_id)

    def restart(self):
        """ Restart rendering
        :return:
        """
        self.frame.evaluateJavaScript("restart();")