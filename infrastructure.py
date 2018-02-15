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

    def add_node(self, node_id, capabilities):
        if node_id in self.nodes.keys() :
            print("Cannot add '" + str(node_id) + "' to the infrastructure. Identifier is already assigned to an existing node.\n" )
        else:
            self.nodes[node_id] = capabilities
            print("Adding '" + str(node_id) + "' to the infrastructure")
            print("\t\t with capabilities: " + str(capabilities) + "\n")
      
    def edit_node(self, node_id, capabilities):
        if node_id in self.things.keys():
            self.nodes[node_id] = capabilities
            print("Editing '" + str(node_id) + "' with capabilities " )
            print("\t\t with capabilities: " + str(capabilities) + "\n")
        else:
            print("Cannot edit '" + str(node_id) + "' since it hasn't been added to the infrastructure yet.\n " )
    
    def delete_node(self, node_id):
        if node_id in self.nodes.keys():
            del self.nodes[node_id]
            print("Deleting '" + str(node_id) + "' from the infrastructure.\n " )
        else:
            print("Cannot delete '" + str(node_id) + "' since it hasn't been added to the infrastructure yet.\n " )

    def add_thing(self, thing_id, thing_type):
        if thing_id in self.things.keys():
            print("Cannot add '" + str(thing_id) + "' to the infrastructure. Identifier is already assigned to an existing node.\n" )
        else:
            self.things[thing_id] = thing_type
            print("Adding '" + str(thing_id) + "' to the infrastructure")
            print("\t\t with type: " + str(thing_type) + "\n")

    def delete_thing(self, thing_id):
        if thing_id in self.things.keys():
            del self.things[thing_id]
            print("Deleting '" + str(thing_id) + "' from the infrastructure.\n " )
        else:
            print("Cannot delete '" + str(thing_id) + "' since it hasn't been added to the infrastructure yet.\n " )

    def get_things(self):
        return json.dumps(self.things)

    def get_nodes(self):
        return json.dumps(self.nodes)

    def get_links(self):
        return self.links
    
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
            return
        if link.endpoint_b in self.things or link.endpoint_b in self.nodes:
            print("Endpoint " + link.endpoint_b + " is a valid endpoint.")
        else:
            print("Endpoint " + link.endpoint_b + " is not a valid endpoint.")
            return
        
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
  
  

I = Infrastructure()

I.add_node("fog_1", [])
print(I.nodes)

I.add_node("fog_2", [])
I.add_node("fog_1", [])

print(I.nodes)
I.edit_node("fog_2", {'hardware' : {'ram' : 4, 'hdd' : 20, 'cpu' : 2}})
I.edit_node("fog_1", {'hardware' : {'ram' : 4, 'hdd' : 20, 'cpu' : 2}})
print(I.nodes)
I.add_link(Link('fog_1', 'fog_2'))
#I.delete_node('fog_2')

I.add_thing("t1", "water")
I.add_thing("t1", "gas")
I.add_thing("t2", "water")
I.add_thing("t3", "broken_thing")
print(I.things)

I.delete_thing("t3")
print(I.things)

b_ab = ProbabilityDistribution([0.5, 0.25, 0.25], [12.0, 6.5, 0.0])
b_ba = ProbabilityDistribution([0.5, 0.25, 0.25], [12.0, 6.0, 0.0])
l = ProbabilityDistribution([0.5, 0.25, 0.25], [50.0, 60.0, 100.0])
q = QoSProfile(b_ab, b_ba, l)
q.sample_qos()

I.sample_links()

I.add_link(Link("fog_1", "fog_2", q))

print(I.get_links())
I.sample_links()
print(I.get_links())

print(I.get_nodes())