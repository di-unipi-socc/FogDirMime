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
            return -1
        else:
            self.published_apps[app_id] = app_description
            print("Publishing '" + str(app_id) + "' to FogDirector")
            print("\t\t with requirements: " + str(app_description) + "\n")
            return 1


    def new_deployment(self, deployment_id, app_id):
        available_deployment_id = self.is_available_deployment_id(deployment_id)
        published_app = self.is_published_app(app_id)

        if available_deployment_id and published_app:
            self.deploying_apps[deployment_id] = Deployment(app_id, self.published_apps[app_id])
            return 1
        else:
            return -1



    def deploy_component(self, deployment_id, component, node):
        if not(deployment_id in self.deploying_apps):
            print("Deployment " + deployment_id + " is not associated to any app being deployed.")
            return -1

        if not(self.is_app_component(component, deployment_id)):
            print("Cannot deploy component '" + str(component) + "' to node '"+ str(node) + "' since it is not part of '" + str(self.deploying_apps[deployment_id].app_id) + "'.")
            return -1

        if component in self.deploying_apps[deployment_id].deployment.keys():
            print("Cannot deploy component '" + str(component) + "' to node '"+ str(node) + "' since it is already deployed to node '" + str(self.deploying_apps[deployment_id].deployment[component]) + "'.")
            return -1
    
        if not(component in self.deploying_apps[deployment_id].deployment.keys()) :
            self.deploying_apps[deployment_id].deployment[component] = node
            print("Deploying component '" + str(component) + "' to node '"+ str(node) +"'.")
            return 1

        

    def bind_thing(self, deployment_id, thing_requirement, thing):
        if not(deployment_id in self.deploying_apps):
            print("Deployment id '" + deployment_id + "' is not associated to any app being deployed.")
            return -1
        if thing_requirement in self.deploying_apps[deployment_id].things_binding:
            print("Cannot bind '" + str(thing_requirement) + "' to '"+ str(thing) + "' since it is already bound to '" + str(self.deploying_apps[deployment_id].things_binding[thing_requirement]) + "'.")
            return -1
        if thing['thing_type'] == self.deploying_apps[deployment_id].app_description['thing_requirements'][thing_requirement]['thing_type']:
            print("Binding '" + str(thing_requirement) + "' to '"+ str(thing) + "'.")
            self.deploying_apps[deployment_id].things_binding[thing_requirement] = thing
            return 1
        else:
            print("Cannot bind '" + str(thing_requirement) + "' to '"+ str(thing) + "' due to type mismatch.")
            return -1

    def unbind_thing(self, deployment_id, thing_requirement):
        if not(deployment_id in self.deploying_apps):
            print("Deployment id '" + deployment_id + "' is not associated to any app being deployed.")
            return -1

        if thing_requirement in self.deploying_apps[deployment_id].things_binding:
            print("Unbinding '" + str(thing_requirement) + "' from '" + str(self.deploying_apps[deployment_id].things_binding[thing_requirement]) + "'.")
            return 1
        else:
            print("Cannot unbind '" + str(thing_requirement) + "' since it is not bound to any Thing.")
            return -1

    def start_app(self, deployment_id):
        if not(deployment_id in self.deploying_apps):
            print("Deployment id '" + deployment_id + "' is not associated to any app being deployed.")
            return -1
        if len(self.deploying_apps[deployment_id].deployment) == len(self.deploying_apps[deployment_id].app_description['components']):
            if len(self.deploying_apps[deployment_id].things_binding) == len(self.deploying_apps[deployment_id].app_description['thing_requirements']):
                print("Starting app deployment '" + deployment_id + "'.")
                deployment = self.deploying_apps[deployment_id]
                del self.deploying_apps[deployment_id]
                self.running_apps[deployment_id] = deployment
                return 1
            else:
                print("Cannot start deployment '" + deployment_id + "' since all thing requirements must be bound first.")
                return -1
        else:
            print("Cannot start deployment '" + deployment_id + "' since all app components must be deployed first.")
            return -1
        

    def stop_app(self, deployment_id):
        if deployment_id in self.deploying_apps:
            print("Deployment id '" + deployment_id + "' corresponds to an already stopped app.")
            return -1
        if not(deployment_id in self.running_apps):
            print("Deployment id '" + deployment_id + "' is not associated to any running app.")
            return -1
        else:
            print("Stopping app deployment '" + deployment_id + "'.")
            deployment = self.running_apps[deployment_id]
            del self.running_apps[deployment_id]
            self.deploying_apps[deployment_id] = deployment
            return 1
            

    def undeploy_component(self, deployment_id, component):
     
        if not(deployment_id in self.deploying_apps) :
            print("Deployment id '" + deployment_id + "' is not associated to any app being deployed.")
            if not(deployment_id in self.running_apps):
                print("Deployment '" + deployment_id + "' is not associated to any running app.")
                return -1
            else:
                print("Deployment '" + deployment_id + "' is currently running. Stop it before undeploying components.")
                return -1
            return -1

        if not(self.is_app_component(component, deployment_id)):
            print("Cannot undeploy component '" + str(component) + "' since it is not part of '" + str(self.deploying_apps[deployment_id].app_id) + "'.")
            return -1
        
        if component in self.deploying_apps[deployment_id].deployment.keys():
            print("Undeploying component '" + str(component) + "' from node '"+ str(self.deploying_apps[deployment_id].deployment[component]) + "'.")
            del self.deploying_apps[deployment_id].deployment[component]
            return 1
        else:
            print("Component '" + str(component) + "' was already undeployed.")
            return -1
    
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
            return 1
        else: 
            return -1
            

        
    def delete_deployment(self, deployment_id):

        if not(deployment_id in self.deploying_apps):
            print("Deployment '"+ str(deployment_id) + "' is not associated to an app currently being deployed or undeployed.")
            return -1

        if deployment_id in self.running_apps:
            print("Deployment '"+ str(deployment_id) + "' is currently running. Stop it before deleting it.")
            return -1
    
        if self.can_delete_deployment(deployment_id):
            print("Deleting deployment '" + str(deployment_id) + "'." )
            del self.deploying_apps[deployment_id]
            return 1
        else:
            print("Cannot delete deployment '" + str(deployment_id) + "'. Some app component(s) must be undeployed first." )
            return -1

    def is_app_component(self, component, deployment_id):
        if (deployment_id in self.deploying_apps):
            return component in self.deploying_apps[deployment_id].app_description['components']
        else: 
            return False
    
    def is_published_app(self, app_id):
        published_app = False
        if app_id in self.published_apps:
            print("'" + str(app_id) + "' is a published app in FogDirector." )
            published_app = True
        else:
            print("'" + str(app_id) + "' must be published to FogDirector before starting a new deployment.\n")
        return published_app

    def is_available_deployment_id(self, deployment_id):
        available_deployment_id = False
        if deployment_id in self.deploying_apps or deployment_id in self.running_apps:
            print("'" + deployment_id +"' is already assigned to an existing deployment in FogDirector.\n")
        else:
            print("'" + deployment_id + "' is available to start a new deployment.")
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

