import random as rnd
import numpy as np
import json
from infrastructure import *

class Deployment():

    def __init__(self, app_id, app_description):
        self.app_id = app_id
        self.app_description = app_description
        self.deployment = {}
        self.things_binding = {}


class AppManager():

    def __init__(self):
        self.published_apps = {}
        self.deploying_apps = {}
        self.running_apps = {}

    def publish_app(self, app_id, app_description):
        if app_id in self.published_apps:
            print("Cannot publish '" + str(app_id) + "' to FogDirector. Identifier is already assigned to a published app.\n" )
        else:
            self.published_apps[app_id] = app_description
            print("Publishing '" + str(app_id) + "' to FogDirector")
            print("\t\t with requirements: " + str(app_description) + "\n")


    def new_deployment(self, deployment_id, app_id):
        available_deployment_id = self.is_available_deployment_id(deployment_id)
        published_app = self.is_published_app(app_id)

        if available_deployment_id and published_app:
            self.deploying_apps[deployment_id] = Deployment(app_id, self.published_apps[app_id])



    def deploy_component(self, deployment_id, component, node):
        if not(deployment_id in self.deploying_apps):
            print("Deployment " + deployment_id + " is not associated to any app being deployed.")
            return

        if not(self.is_app_component(component, deployment_id)):
            print("Cannot deploy component '" + str(component) + "' to node '"+ str(node) + "' since it is not part of '" + str(self.deploying_apps[deployment_id].app_id) + "'.")
            return
    
        if not(component in self.deploying_apps[deployment_id].deployment.keys()) :
            self.deploying_apps[deployment_id].deployment[component] = node
            print("Deploying component '" + str(component) + "' to node '"+ str(node) +"'.")
            return

        if component in self.deploying_apps[deployment_id].deployment.keys():
            print("Cannot deploy component '" + str(component) + "' to node '"+ str(node) + "' since it is already deployed to node '" + str(self.deploying_apps[deployment_id].deployment[component]) + "'.")
            return

    def bind_thing(self, deployment_id, thing_requirement, thing):
        if not(deployment_id in self.deploying_apps):
            print("Deployment id '" + deployment_id + "' is not associated to any app being deployed.")
            return
        if thing_requirement in self.deploying_apps[deployment_id].things_binding:
            print("Cannot bind '" + str(thing_requirement) + "' to '"+ str(thing) + "' since it is already bound to '" + str(self.deploying_apps[deployment_id].things_binding[thing_requirement]) + "'.")
        if thing['thing_type'] == self.deploying_apps[deployment_id].app_description['thing_requirements'][thing_requirement]['thing_type']:
            print("Binding '" + str(thing_requirement) + "' to '"+ str(thing) + "'.")
            self.deploying_apps[deployment_id].things_binding[thing_requirement] = thing
        else:
            print("Cannot bind '" + str(thing_requirement) + "' to '"+ str(thing) + "' due to type mismatch.")

    def unbind_thing(self, deployment_id, thing_requirement):
        if not(deployment_id in self.deploying_apps):
            print("Deployment id '" + deployment_id + "' is not associated to any app being deployed.")
            return 

        if thing_requirement in self.deploying_apps[deployment_id].things_binding:
            print("Unbinding '" + str(thing_requirement) + "' from '" + str(self.deploying_apps[deployment_id].things_binding[thing_requirement]) + "'.")
        else:
            print("Cannot unbind '" + str(thing_requirement) + "' since it is not bound to any Thing.")

    def start_app(self, deployment_id):
        if not(deployment_id in self.deploying_apps):
            print("Deployment id '" + deployment_id + "' is not associated to any app being deployed.")
            return
        if len(self.deploying_apps[deployment_id].deployment) == len(self.deploying_apps[deployment_id].app_description['components']):
            if len(self.deploying_apps[deployment_id].things_binding) == len(self.deploying_apps[deployment_id].app_description['thing_requirements']):
                print("Starting app deployment '" + deployment_id + "'.")
                deployment = self.deploying_apps[deployment_id]
                del self.deploying_apps[deployment_id]
                self.running_apps[deployment_id] = deployment
            else:
                print("Cannot start deployment '" + deployment_id + "' since all thing requirements must be bound first.")
        else:
            print("Cannot start deployment '" + deployment_id + "' since all app components must be deployed first.")
        return

    def stop_app(self, deployment_id):
        if not(deployment_id in self.running_apps):
            print("Deployment id '" + deployment_id + "' is not associated to any running app.")
            return
        else:
            print("Stopping app deployment '" + deployment_id + "'.")
            deployment = self.running_apps[deployment_id]
            del self.running_apps[deployment_id]
            self.deploying_apps[deployment_id] = deployment
            

    def undeploy_component(self, deployment_id, component):
     
        if not(deployment_id in self.deploying_apps) :
       
            print("Deployment id '" + deployment_id + "' is not associated to any app being deployed.")
        
            if not(deployment_id in self.running_apps):
                print("Deployment '" + deployment_id + "' is not associated to any running app.")
            else:
                print("Deployment '" + deployment_id + "' is currently running. Stop it before undeploying components.")
            return

        if not(self.is_app_component(component, deployment_id)):
            print("Cannot undeploy component '" + str(component) + "' since it is not part of '" + str(self.deploying_apps[deployment_id].app_id) + "'.")
            return
        
        if component in self.deploying_apps[deployment_id].deployment.keys():
            print("Undeploying component '" + str(component) + "' from node '"+ str(self.deploying_apps[deployment_id].deployment[component]) + "'.")
            del self.deploying_apps[deployment_id].deployment[component]
            return
        else:
            print("Component '" + str(component) + "' was already undeployed.")
    
    def unpublish_app(self, app_id):
        unpublish = True

        for app in self.deploying_apps:
            if self.deploying_apps[app].app_id == app_id :
                print("The app is currently being deployed and it cannot be unpublished - " +  app)
                unpublish = False

        for app in self.running_apps:
            if self.running_apps[app].app_id == app_id :
                print("The app is currently running and it cannot be unpublished."  +  app)
                unpublish = False

        if unpublish:
            print("Unpublishing '" + app_id + "'.")
            del self.published_apps[app_id]
            

        
    def delete_deployment(self, deployment_id):

        if not(deployment_id in self.deploying_apps):
            print("Deployment '"+ str(deployment_id) + "' is not associated to an app currently being deployed or undeployed.")
            return

        if deployment_id in self.running_apps:
            print("Deployment '"+ str(deployment_id) + "' is currently running. Stop it before deleting it.")
            return
    
        if self.can_delete_deployment(deployment_id):
            print("Deleting deployment '" + str(deployment_id) + "'." )
            del self.deploying_apps[deployment_id]
            return
        else:
            print("Cannot delete deployment '" + str(deployment_id) + "'. Some app component(s) must be undeployed first." )
            return

    def is_app_component(self, component, deployment_id):
        if (deployment_id in self.deploying_apps):
            return component in self.deploying_apps[deployment_id].app_description['components']
        else: 
            return False
    
    def is_published_app(self, app_id):
        published_app = False
        if app_id in self.published_apps:
            print("'" + str(app_id) + "' is a published app in FogDirector.\n" )
            published_app = True
        else:
            print("'" + str(app_id) + "' must be published to FogDirector before starting a new deployment.\n")
        return published_app

    def is_available_deployment_id(self, deployment_id):
        available_deployment_id = False
        if deployment_id in self.deploying_apps or deployment_id in self.running_apps:
            print("'" + deployment_id +"' is already assigned to an existing deployment in FogDirector.\n")
        else:
            print("'" + deployment_id + "' is available to start a new deployment.\n")
            available_deployment_id = True
        return available_deployment_id

    def can_delete_deployment(self, deployment_id):
        return not(self.deploying_apps[deployment_id].deployment)

    def get_published_apps(self):
        return json.dumps(self.published_apps)

    def get_deploying_apps(self):
        return json.dumps(self.deploying_apps)

    def get_running_apps(self):
        return json.dumps(self.running_apps)


# fd = AppManager()

# fd.publish_app("app1", {'components' : {'A' : {'hardware' : {'ram' : 1, 'hdd' : 5, 'cpu' : 1}}},"thing_requirements" : [{'component': 'A', 'thing_type': 'water', 'qos_profile' : {'latency' : 15, 'bw_c2t': 0.5, 'bw_t2c' : 1} }]})
# fd.new_deployment("dep1", "app1")
# fd.deploy_component("dep1", 'A', "fog2")
# fd.bind_thing("dep1", 0, {'thing_id' : "water1", 'thing_type': 'water'})
# fd.bind_thing("dep1", 0, {'thing_id' : "water1", 'thing_type': 'water'})
# fd.start_app("dep1")
# fd.unpublish_app("app1")
# fd.stop_app("dep1")
# fd.undeploy_component("dep1", 'A')
# fd.unpublish_app("app1")
# fd.delete_deployment("dep1")
# fd.unpublish_app("app1")


# fd.publish_app("app2", [])
# fd.publish_app("app1", [])

# fd.new_deployment("dep1", "app3")

# fd.delete_deployment("dep1")

# fd.new_deployment("dep1bis", "app1")
# print(fd.deploying_apps['dep1bis'].app_description['thing_requirements'])
# fd.deploy_component("dep1bis", 'A', "fog1")
# fd.bind_thing("dep1bis", 0, {'thing_id' : "water1", 'thing_type': 'water'})


# fd.undeploy_component("dep1bis", "A")
# fd.undeploy_component("dep1bis", "A")
# fd.deploy_component("dep1bis", 'B', "fog1")
# fd.delete_deployment("dep1bis")

