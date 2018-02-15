from app_manager import *
from infrastructure import *

class FogDirSim():
    def __init__(self):
        self.infrastructure = Infrastructure()
        self.app_manager = AppManager()

    def add_node(self, node_id, capabilities):
        self.infrastructure.add_node(node_id, capabilities)

    def edit_node(self, node_id, capabilities):
        self.infrastructure.edit_node(node_id, capabilities)

    def delete_node(self, node_id):
        self.infrastructure.delete_node(node_id)

    def add_thing(self, thing_id, thing_type):
        self.infrastructure.add_thing(thing_id, thing_type)

    def delete_thing(self, thing_id):
        self.infrastructure.delete_thing(thing_id)

    def publish_app(self, app_id,app_description):
        self.app_manager.publish_app(app_id, app_description)

    def new_deployment(self, deployment_id, app_id):
        self.app_manager.new_deployment(deployment_id, app_id) 

    def deploy_component(self, deployment_id, component, node ):
        app = self.app_manager.deploying_apps[deployment_id].app_description
        component_requirements = app['components'][component]

        if node in self.infrastructure.nodes and self.can_support(component_requirements, node):
            print("Node '"+ node +"' can accomodate component '"+ component +"'.")
            self.app_manager.deploy_component(deployment_id, component, node)
            self.edit_node(node, self.install(component_requirements, node))
        else:
            print("Node '"+ node +"' cannot accomodate component '"+ component +"'.")
            
    def install(self, component_requirements, node):
        cr = component_requirements['hardware']
        n = self.infrastructure.nodes[node]['hardware']
        remaining = {'hardware':{}}
        r = remaining['hardware']
        r['ram'] = n['ram']-cr['ram']
        r['hdd'] = n['hdd']-cr['hdd']
        r['cpu'] = n['cpu']-cr['cpu']
        return remaining
    
    def can_support(self, component_requirements, node):
        cr = component_requirements['hardware']
        n = self.infrastructure.nodes[node]['hardware']
        return cr['ram'] <= n['ram'] and cr['hdd'] <= n['hdd'] and cr['cpu'] <= n['cpu']
        
    def bind_thing(self, deployment_id, thing_requirement, thing_id):
        
        if thing_id in self.infrastructure.things:
            thing_type = self.infrastructure.things[thing_id]
            t = {}
            t['thing_id'] = thing_id
            t['thing_type'] = thing_type
            print("Thing '"+ thing_id + "' is available in the infrastructure.")
            self.app_manager.bind_thing(deployment_id, thing_requirement, t)
        else:
            print("Thing '"+ thing_id + "' is not available in the infrastructure.")
        
    def start_app(self, deployment_id):
        self.app_manager.start_app(deployment_id)
    
    def stop_app(self, deployment_id):
        self.app_manager.stop_app(deployment_id)
    
    def unbind_thing(self, deployment_id, thing_requirement):
        self.app_manager.unbind_thing(deployment_id, thing_requirement)
    
    def undeploy_component(self, deployment_id, component):
        self.app_manager.undeploy_component(deployment_id, component)

    def uninstall(self, component_requirements, node):
        cr = component_requirements['hardware']
        n = self.infrastructure.nodes[node]['hardware']
        remaining = {'hardware':{}}
        r = remaining['hardware']
        r['ram'] = n['ram']+cr['ram']
        r['hdd'] = n['hdd']+cr['hdd']
        r['cpu'] = n['cpu']+cr['cpu']
        return remaining
    
    def delete_deployment(self, deployment_id):
        self.app_manager.delete_deployment(deployment_id)
    
    def unpublish_app(self, app_id):
        self.app_manager.unpublish_app(app_id)

    def get_published_apps(self):
        self.app_manager.get_published_apps()

    def get_deploying_apps(self):
        self.app_manager.get_deploying_apps()

    def get_running_apps(self):
        self.app_manager.get_running_apps()

    def get_things(self):
        self.infrastructure.get_things()

    def get_nodes(self):
        self.infrastructure.get_nodes()

    def get_links(self):
        self.infrastructure.get_links()

    def check_resource_alert(self, deployment_id):
        resource_alerts = []
        return resource_alerts
    
    def check_c2t_alert(self, deployment_id):
        resource_alerts = []

        return resource_alerts
    
    def check_c2c_alert(self, deployment_id):
        resource_alerts = []
        return resource_alerts

    def get_alert(self, deployment_id):
        alerts = []
        alerts.append(self.check_resource_alert(deployment_id))
        alerts.append(self.check_c2t_alert(deployment_id))
        alerts.append(self.check_c2c_alert(deployment_id))
        return alerts


fd = FogDirSim()
fd.add_node("fog_2", {'hardware' : {'ram' : 4, 'hdd' : 20, 'cpu' : 2}})
fd.add_thing("water0", "water")
app = {"components" :  {"ThingsController" : {"hardware" : {"ram" : 1, "hdd" : 2, "cpu" : 1}}, "DataStorage" : {"hardware" : {"ram" : 2, "hdd" : 30, "cpu" : 1}}}, "thing_requirements" :  [{"component": "ThingsController", "thing_type": "temperature", "qos_profile" : {"latency" : 500, "bw_c2t": 0.1, "bw_t2c" : 0.1} }, {"component": "ThingsController", "thing_type": "fire", "qos_profile" : {"latency" : 50, "bw_c2t": 0.1, "bw_t2c" : 0.1} } ], "link_requirements" : [ {"component_a" : "ThingsController", "component_b" : "DataStorage", "qos_profile" : {"latency" : 160, "bw_ab": 0.7, "bw_ba" : 0.5} }]}
fd.publish_app("app1", app)
fd.new_deployment("dep1", "app1")
fd.deploy_component("dep1", "ThingsController", "fog_2")
fd.bind_thing("dep1", 0, "water0")  
# fd.bind_thing("dep1", 0, "water2") 
fd.unbind_thing("dep1", 0)

