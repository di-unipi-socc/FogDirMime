import random as rnd
import numpy as np
import json


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
        try:
            self.nodes[node_id] = capabilities
            print("Editing '" + str(node_id) + "' with capabilities " )
            print("\t\t with capabilities: " + str(capabilities) + "\n")
        except KeyError:
            print("Cannot edit '" + str(node_id) + "' since it hasn't been added to the infrastructure yet.\n " )
    
    def delete_node(self, node_id):
        try:
            del self.nodes[node_id]
            print("Deleting '" + str(node_id) + "' from the infrastructure.\n " )
        except KeyError:
            print("Cannot delete '" + str(node_id) + "' since it hasn't been added to the infrastructure yet.\n " )

    def add_thing(self, thing_id, thing_type):
        try:
            retrieve_thing = self.things[thing_id]
            print("Cannot add '" + str(thing_id) + "' to the infrastructure. Identifier is already assigned to an existing node.\n" )
        except KeyError:
            self.things[thing_id] = thing_type
            print("Adding '" + str(thing_id) + "' to the infrastructure")
            print("\t\t with type: " + str(thing_type) + "\n")

    def delete_thing(self, thing_id):
        try:
            del self.things[thing_id]
            print("Deleting '" + str(thing_id) + "' from the infrastructure.\n " )
        except KeyError:
            print("Cannot delete '" + str(thing_id) + "' since it hasn't been added to the infrastructure yet.\n " )

    def get_things(self):
        return json.dumps(self.things)

    def get_nodes(self):
        return json.dumps(self.nodes)

    def get_links(self):
        return json.dumps(self.links)

    # def add_link(self, endpoint_a, endpoint_b, qos_profile):
    # TODO
  

# I = Infrastructure()

# I.add_node("fog_1", [])
# print(I.nodes)

# I.add_node("fog_2", [])
# I.add_node("fog_1", [])

# print(I.nodes)
# I.edit_node("fog_2", {'hardware' : {'ram' : 4, 'hdd' : 20, 'cpu' : 2}})
# I.edit_node("fog_1", {'hardware' : {'ram' : 4, 'hdd' : 20, 'cpu' : 2}})
# print(I.nodes)
# I.del_node('fog_2')

# I.add_thing("t1", "water")
# I.add_thing("t1", "gas")
# I.add_thing("t2", "water")
# I.add_thing("t3", "broken_thing")
# print(I.things)

# I.del_thing("t3")
# print(I.things)

# print(I.get_nodes())