import random as rnd
import numpy as np
import json
from qos import *


class Infrastructure():
    """Infrastructure management."""
    def __init__(self):
        self.things = {}
        self.nodes = {}
        self.links = {}

    def add_node(self, node):
        node_id = node.node_id
        if node_id in self.nodes.keys() :
            print("Cannot add '" + str(node_id) + "' to the infrastructure. Identifier is already assigned to an existing node.\n" )
            return -1
        else:
            self.nodes[node_id] = node
            print("Adding '" + str(node_id) + "' to the infrastructure.")
            return 1
      
    def edit_node(self, node):
        node_id = node.node_id
        if node_id in self.nodes.keys():
            self.nodes[node_id] = node
            print("Editing '" + str(node_id) + "'." )
            return 1
        else:
            print("Cannot edit '" + str(node_id) + "' since it hasn't been added to the infrastructure yet.\n " )
            return -1
    
    def delete_node(self, node_id):
        if node_id in self.nodes.keys():
            del self.nodes[node_id]
            print("Deleting '" + str(node_id) + "' from the infrastructure.\n " )
            return 1
        else:
            print("Cannot delete '" + str(node_id) + "' since it hasn't been added to the infrastructure yet.\n " )
            return -1

    def add_thing(self, thing_id, thing_type):
        if thing_id in self.things.keys():
            print("Cannot add '" + str(thing_id) + "' to the infrastructure. Identifier is already assigned to an existing thing.\n" )
            return -1
        else:
            self.things[thing_id] = thing_type
            print("Adding '" + str(thing_id) + "' to the infrastructure.")
            return 1

    def delete_thing(self, thing_id):
        if thing_id in self.things.keys():
            del self.things[thing_id]
            print("Deleting '" + str(thing_id) + "' from the infrastructure.\n " )
            return 1
        else:
            print("Cannot delete '" + str(thing_id) + "' since it hasn't been added to the infrastructure yet.\n " )
            return -1

    def get_things(self):
        return json.dumps(self.things)

    def get_nodes(self):
        return json.dumps(self.nodes)

    def get_links(self):
        return self.links

    def sample_resources(self):
        for node in self.nodes.values():
            node.sample_resources()
    
    def sample_links(self):
        for e1 in self.links.keys():
            adj_list = self.links[e1].keys()
            for e2 in adj_list:
                self.links[e1][e2]['bandwidth'].sample_value()
                self.links[e1][e2]['latency'].sample_value()


    def add_link(self, link):
        if link.endpoint_a in self.things or link.endpoint_a in self.nodes:
            print("Endpoint " + link.endpoint_a + " is a valid endpoint.")
        else:
            print("Endpoint " + link.endpoint_a + " is not a valid endpoint.")
            return -1
        if link.endpoint_b in self.things or link.endpoint_b in self.nodes:
            print("Endpoint " + link.endpoint_b + " is a valid endpoint.")
        else:
            print("Endpoint " + link.endpoint_b + " is not a valid endpoint.")
            return -1
        
        print("Adding link between " + link.endpoint_a + " and " + link.endpoint_b)

        if not(link.endpoint_a in self.links.keys()):
            self.links[link.endpoint_a] = {}
        if not(link.endpoint_b in self.links.keys()):
            self.links[link.endpoint_b] = {}

        if not (link.endpoint_b in self.links[link.endpoint_a]):
            self.links[link.endpoint_a][link.endpoint_b] = {}
        if not (link.endpoint_a in self.links[link.endpoint_b]):
            self.links[link.endpoint_b][link.endpoint_a] = {}

        self.links[link.endpoint_a][link.endpoint_b]['bandwidth'] = link.qos_profile.bandwidth_ab
        self.links[link.endpoint_b][link.endpoint_a]['bandwidth'] = link.qos_profile.bandwidth_ba
        self.links[link.endpoint_a][link.endpoint_b]['latency'] = link.qos_profile.latency
        self.links[link.endpoint_b][link.endpoint_a]['latency'] = link.qos_profile.latency

        return 1
  
  
