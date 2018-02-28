from app_manager import *
from infrastructure import *
import random as rnd

class FogDirSim():
    def __init__(self):
        self.infrastructure = Infrastructure()
        self.app_manager = AppManager()
        self.stuck = {}
        self.alerts = {}

    def add_node(self, node):
        self.infrastructure.add_node(node)

    def edit_node(self, node):
        self.infrastructure.edit_node(node)

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
    
    def add_link(self, link):
        return self.infrastructure.add_link(link)

    def deploy_component(self, deployment_id, component, node_id):
        self.infrastructure.sample_resources()
        app = self.app_manager.deploying_apps[deployment_id].app_description
        deployment = self.app_manager.deploying_apps[deployment_id].deployment
        component_requirements = app['components'][component]

        if component in deployment:
            print("Cannot deploy" + component +", it is already deployed.")
            return

        if node_id in self.infrastructure.nodes and self.can_support(component_requirements, node_id):
            print("Node '"+ node_id +"' can accomodate component '"+ component +"'.")
            self.app_manager.deploy_component(deployment_id, component, node_id)
            self.install(component_requirements, node_id)
        else:
            print("Node '"+ node_id +"' cannot accomodate component '"+ component +"'.")
            
    def install(self, component_requirements, node_id):
        cr = component_requirements['hardware']
        n = self.infrastructure.nodes[node_id]
        n.used_ram = n.used_ram + cr['ram']
        n.used_hdd = n.used_hdd + cr['hdd']
        n.used_cpu = n.used_cpu + cr['cpu']
        
    
    def can_support(self, component_requirements, node_id):
        cr = component_requirements['hardware']
        n = self.infrastructure.nodes[node_id]
        return cr['ram'] <= n.get_available_ram() and cr['hdd'] <= n.get_available_hdd() and cr['cpu'] <= n.get_available_cpu()
        
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
        app = self.app_manager.deploying_apps[deployment_id].app_description
        deployment = self.app_manager.deploying_apps[deployment_id].deployment
        component_requirements = app['components'][component]

        if component in deployment:
            node_id = deployment[component]
            del deployment[component]
            self.app_manager.undeploy_component(deployment_id, component)
            self.uninstall(component_requirements, node_id)
            print("Undeploying '" + component +"'.")
            return
        else:
            print("Component " + component + " to be undepoyed is not part of deployment "+ deployment_id)

    def uninstall(self, component_requirements, node_id):
        cr = component_requirements['hardware']
        n = self.infrastructure.nodes[node_id]
        n.used_ram = n.used_ram - cr['ram']
        n.used_hdd = n.used_hdd - cr['hdd']
        n.used_cpu = n.used_cpu - cr['cpu']
    
    def delete_deployment(self, deployment_id):
        return self.app_manager.delete_deployment(deployment_id)
    
    def unpublish_app(self, app_id):
        return self.app_manager.unpublish_app(app_id)

    def get_published_apps(self):
        return self.app_manager.get_published_apps()

    def get_deploying_apps(self):
        return self.app_manager.get_deploying_apps()

    def get_running_apps(self):
        return self.app_manager.get_running_apps()

    def get_things(self):
        return self.infrastructure.get_things()

    def get_nodes(self):
        self.infrastructure.sample_resources()
        return self.infrastructure.get_nodes()

    def get_links(self):
        self.infrastructure.sample_links()
        return self.infrastructure.get_links()

    def check_resource_alert(self, deployment_id):
        alerts = []
        deployment = self.app_manager.running_apps[deployment_id].deployment
        for component in deployment.keys():
            print(component)
            node = self.infrastructure.nodes[deployment[component]]
            if (
                node.get_available_cpu() < 0 
                or node.get_available_hdd() < 0 
                or node.get_available_ram() < 0
                ):
                print("no resources")
                alerts.append({"alert_type":"resources", "component": component})
        return alerts
    
    def check_c2t_alert(self, deployment_id):
        alerts = []
        deployment = self.app_manager.running_apps[deployment_id]
        i = 0
        for tr in deployment.app_description['thing_requirements']:
            q = tr['qos_profile']
            thing = deployment.things_binding[i]['thing_id']
            node = deployment.deployment[tr['component']]
            links = self.infrastructure.links
            if (
                not(links[node][thing]['bandwidth'].value >= q['bw_c2t'] 
                and links[thing][node]['bandwidth'].value >= q['bw_t2c'] 
                and links[node][thing]['latency'].value <= q['latency'] 
                and links[thing][node]['latency'].value <= q['latency'])
                ):
                alerts.append({"alert_type":"c2t", "component": node, "thing": thing})
        return alerts
    
    def check_c2c_alert(self, deployment_id):
        alerts = []
        deployment = self.app_manager.running_apps[deployment_id]
        for lr in deployment.app_description["link_requirements"]:
            a = lr['component_a']
            b = lr['component_b']
            node_a = deployment.deployment[a]
            node_b = deployment.deployment[b]
            q = lr['qos_profile']
            if (
                node_a != node_b 
                and not(self.infrastructure.links[node_a][node_b]['bandwidth'].value >= q['bw_ab'] 
                and self.infrastructure.links[node_b][node_a]['bandwidth'].value >= q['bw_ba'] 
                and self.infrastructure.links[node_a][node_b]['latency'].value <= q['latency'] 
                and self.infrastructure.links[node_b][node_a]['latency'].value <= q['latency'])
                ):
                alerts.append({"alert_type":"c2c", "c1": a, "c2": b})

        return alerts
    
    def sample_state(self):
        self.infrastructure.sample_links()
        self.infrastructure.sample_resources()

    def get_alert(self, deployment_id):
        if not(deployment_id in self.app_manager.running_apps):
            print("Deployment '"+ str(deployment_id) + "' is not associated to an app currently running.")
            return 
        alerts = []
        self.sample_state()
        self.infrastructure.sample_links()
        self.infrastructure.sample_resources()
        alerts= alerts + (self.check_resource_alert(deployment_id))
        alerts = alerts + (self.check_c2t_alert(deployment_id))
        alerts = alerts + (self.check_c2c_alert(deployment_id))
        return alerts
