import random as rnd
import venv
import numpy as np
import json

class ProbabilityDistribution():
    
    def __init__(self, probabilities = [1], values = [0]):
        self.probabilities = probabilities
        self.values = values
        self.value = -1.0
        
    def sample_value(self):
        self.value = float(np.random.choice(self.values, p = self.probabilities))

    def __repr__(self):
        return json.dumps({"probabilities": self.probabilities, "values": self.values, "value": self.value})
    
    def __dict__(self):
        return {"probabilities": self.probabilities, "values": self.values, "value": self.value}

# #TESTS
# p = ProbabilityDistribution([0.5, 0.5], [1.0, 0.0])
# for i in range(0,10):
#     p.sample_value()
#     print(p.value)
#     print(p)


class HardwareResources():
    
    def __init__(self, ram = ProbabilityDistribution(), hdd = ProbabilityDistribution(), cpu = ProbabilityDistribution() ):
        self.ram = ram
        self.hdd = hdd
        self.cpu = cpu
    
    def sample_resources(self):
        self.ram.sample_value()
        self.cpu.sample_value()
        self.hdd.sample_value()
    
    def get_ram(self):
        return self.ram.value
    
    def get_hdd(self):
        return self.hdd.value
    
    def get_cpu(self):
        return self.cpu.value


class Node():
    
    def __init__(self, node_id = '', resources = HardwareResources(), software = []):
        self.node_id = node_id
        self.resources = resources
        self.software = software
        self.used_ram = 0
        self.used_hdd = 0
        self.used_cpu = 0  
    
    def sample_resources(self):
        self.resources.sample_resources()

    def get_available_ram(self):
        return self.resources.get_ram() - self.used_ram
    
    def get_available_hdd(self):
        return self.resources.get_hdd() - self.used_hdd
    
    def get_available_cpu(self):
        return self.resources.get_cpu() - self.used_cpu



class QoSProfile:

    def __init__(self, bandwidth_ab = ProbabilityDistribution(), bandwidth_ba = ProbabilityDistribution(), latency = ProbabilityDistribution()):
        self.bandwidth_ab = bandwidth_ab
        self.bandwidth_ba = bandwidth_ba
        self.latency = latency
     
    def sample_qos(self):
        self.bandwidth_ab.sample_value()
        self.bandwidth_ba.sample_value()
        self.latency.sample_value()
    
    def get_bandwidth_ab(self):
        return self.bandwidth_ab.value

    def get_bandwidth_ba(self):
        return self.bandwidth_ba.value
    
    def get_latency(self):
        return self.latency.value
    
    
    def __repr__(self):
       return str({"bandwidth_ab": self.bandwidth_ab, "bandwidth_ba": self.bandwidth_ba, "latency": self.latency})
        

# # #TEST
# b_ab = ProbabilityDistribution([0.5, 0.25, 0.25], [12.0, 6.5, 0.0])
# b_ba = ProbabilityDistribution([0.5, 0.25, 0.25], [12.0, 6.0, 0.0])
# l = ProbabilityDistribution([0.5, 0.25, 0.25], [50.0, 60.0, 100.0])

# q = QoSProfile(b_ab, b_ba, l)
# q.sample_qos()

# for i in range(0,100):
#     print("***")
#     q.sample_qos()
#     print(q.get_bandwidth_ba())
#     print(q.get_bandwidth_ab())
#     print(q.get_latency())
    
                 
class Link():
    
    def __init__(self, endpoint_a = '', endpoint_b = '', qos_profile = QoSProfile()):
        self.endpoint_a = endpoint_a
        self.endpoint_b = endpoint_b
        self.qos_profile = qos_profile
    
    def sample_qos(self):
        self.qos_profile.sample_qos()
    
    
    def __repr__(self):
        b_ab = self.qos_profile.get_bandwidth_ab()
        b_ba = self.qos_profile.get_bandwidth_ba()
        l = self.qos_profile.get_latency()
        return json.dumps({"endpoint_a": self.endpoint_a, "endpoint_b": self.endpoint_b, "qos_profile": {'bandwidth_ab': b_ab, 'bandwidth_ba': b_ba, 'latency': l }})
        

# link = Link("A", "B", q)
# for i in range(0,10):
#     link.sample_qos()
#     print(link)

# # print(ProbabilityDistribution().toJSON())

# # def jdefault(o):
# #     return o.__dict__

# # print(json.dumps(QoSProfile(), default=jdefault))