import random as rnd
import venv
import numpy as np
import json

class ProbabilityDistribution():
    
    def __init__(self, probabilities = [1], values = [0]):
        self.probabilities = probabilities
        self.values = values
        self.value = self.sample_value()
            
    def sample_value(self):
        self.value = np.random.choice(self.values, p = self.probabilities)
        #print("Sampling value: " + str(self.value))
        
    def toJSON(self):
        return '{ "probabilities" : ' + (json.dumps(self.probabilities)) + ', "values" : ' + json.dumps(self.values) + '}'
    
    def fromJSON(self, json_string):
        self.probabilities = json_string['probabilities']
        self.values = json_string['values']
        
    
class QoSProfile:

    def __init__(self, bandwidth_ab = ProbabilityDistribution(), bandwidth_ba = ProbabilityDistribution(), latency = ProbabilityDistribution()):
        self.bandwidth_ab = bandwidth_ab
        self.bandwidth_ba = bandwidth_ba
        self.latency = latency
     
    def sample_qos(self):
        try:
            self.bandwidth_ab.sample_value()
        except ValueError:
            print("Error: probabilities in bandwidth_ab do not sum to 1!")
        try:
            self.bandwidth_ba.sample_value()
        except ValueError:
            print("Error: probabilities in bandwidth_ba do not sum to 1!")
        try:
            self.latency.sample_value()
        except ValueError:
            print("Error: probabilities in latency do not sum to 1!")
            
    def toJSON(self):
        return '{ "bandwidth_ab" :'  + json.dumps(self.bandwidth_ab) + ', "bandwidth_ba" : ' + json.dumps(self.bandwidth_ba) + ', "latency" : ' + json.dumps(self.latency.toJSON()) + '}'
    
    def fromJSON(self, profile):
        self.bandwidth_ab.fromJSON(profile['bandwidth_ab'])
        self.bandwidth_ba.fromJSON(profile['bandwidth_ba'])
        self.latency.fromJSON(profile['latency'])
                 
class Link():
    
    def __init__(self, endpoint_a = '', endpoint_b = '', qos_profile = QoSProfile()):
        self.endpoint_a = endpoint_a
        self.endpoint_b = endpoint_b
        self.qos_profile = qos_profile
    
    def get_bandwidth(self, endpoint_x, endpoint_y):
        if (endpoint_x == self.endpoint_a and endpoint_y == self.endpoint_b):
            return self.qos_profile.bandwidth_ab
        elif (endpoint_x == self.endpoint_b and endpoint_y == self.endpoint_a):
            return self.qos_profile.bandwidth_ba
        else:
            print("Invalid input to get_bandwidth for link (" + self.endpoint_a +", " + self.endpoint_b + ")." )
    
    def get_latency(self):
        return 
        
    def toJSON(self):
        return '{ "endpoint_a": "' + self.endpoint_a + '" , "endpoint_b" : "' + self.endpoint_b + '", "qos_profile" : ' + self.qos_profile.toJSON() + ' }'
        
    def fromJSON(self, json_string):
        profile = json.loads(json_string)
        self.endpoint_a = profile['endpoint_a']
        self.endpoint_b = profile['endpoint_b']
        self.qos_profile.fromJSON(profile['qos_profile'])     


print(json.dumps(ProbabilityDistribution()))