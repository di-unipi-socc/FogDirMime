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
    
    def get_bandwidth(self, endpoint_x, endpoint_y):
        if (endpoint_x == self.endpoint_a and endpoint_y == self.endpoint_b):
            return self.qos_profile.get_bandwidth_ab()
        elif (endpoint_x == self.endpoint_b and endpoint_y == self.endpoint_a):
            return self.qos_profile.get_bandwidth_ba()
        else:
            print("Invalid input to get_bandwidth for link (" + self.endpoint_a +", " + self.endpoint_b + ")." )
    
    def get_latency(self):
        return 
    
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