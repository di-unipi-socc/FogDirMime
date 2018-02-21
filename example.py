from fog_director import *

fd = FogDirSim()

fd.add_thing("fire0", "fire")
fd.add_thing("temperature0", "temperature")
fd.add_thing("water0", "water")
fd.add_thing("video0", "video")

#fog_1
hdd = ProbabilityDistribution([0.5, 0.20, 0.20, 0.10],[32.0, 28.0, 20.0, 16.0])
ram = ProbabilityDistribution([0.5, 0.20, 0.20, 0.10],[4.0, 3.0, 2.0, 1.0])
cpu = ProbabilityDistribution([0.7, 0.3],[2.0, 1.0])
hw = HardwareResources(ram, hdd, cpu)
fog_1 = Node("fog_1", hw, ["linux", "php", "sql"])
fd.add_node(fog_1)

#fog_2
hdd2 = ProbabilityDistribution([0.5, 0.20, 0.20, 0.10],[32.0, 28.0, 20.0, 16.0])
ram2 = ProbabilityDistribution([0.5, 0.20, 0.20, 0.10],[2.0, 1.7, 1.5, 1.0])
cpu2 = ProbabilityDistribution([0.7, 0.3],[2.0, 1.0])
hw2 = HardwareResources(ram2, hdd2, cpu2)
fog_2 = Node("fog_2", hw2, ["linux", "php"])
fd.add_node(fog_2)

#fog3
hdd3 = ProbabilityDistribution([0.5, 0.20, 0.20, 0.10],[128.0, 100.0, 70.0, 50.0])
ram3 = ProbabilityDistribution([0.5, 0.20, 0.20, 0.10],[12.0, 10.0, 8.0, 6.0])
cpu3 = ProbabilityDistribution([0.7, 0.3],[4.0, 2.0])
hw3 = HardwareResources(ram3, hdd3, cpu3)
fog_3 = Node("fog_3", hw3, ["linux", "sql"])
fd.add_node(fog_3)


print(fd.infrastructure.nodes["fog_1"].get_available_ram())
print(fd.infrastructure.nodes["fog_2"].get_available_ram())

b_ab = ProbabilityDistribution([0.5, 0.25, 0.25], [12.0, 6.5, 0.0])
b_ba = ProbabilityDistribution([0.5, 0.25, 0.25], [12.0, 6.0, 0.0])
l = ProbabilityDistribution([0.5, 0.25, 0.25], [40.0, 45.0, 100.0])
q = QoSProfile(b_ab, b_ba, l)
q.sample_qos()

fd.add_link(Link("fog_1", "fog_2", q))


fd.add_link(Link("fog_1", "fire0", q) )
fd.add_link(Link("fog_1", "temperature0", q) )
fd.add_link(Link("fog_2", "fire0", q) )
fd.add_link(Link("fog_2", "temperature0", q) )

print(fd.infrastructure.links)

fd.sample_state()

filename = "app.json"
app = {}
with open(filename) as file_object:
    app = json.load(file_object) 
print(app)
fd.publish_app("app1", app)
fd.new_deployment("dep1", "app1")
fd.deploy_component("dep1", "ThingsController", "fog_1")
fd.bind_thing("dep1", 0, "temperature0")  
fd.bind_thing("dep1", 1, "fire0") 
fd.bind_thing("dep1", 2, "video0") 
fd.bind_thing("dep1", 3, "water0") 
fd.deploy_component("dep1", "DataStorage", "fog_3")
fd.deploy_component("dep1", "Dashboard", "fog_2")
fd.start_app("dep1")

runs = 10

alert_no = 0
for i in range(0, runs):
    fatto = False
    alerts=fd.get_alert("dep1")
    print("****" + str(alerts))
    #print(alert_no)
    if alerts is not None and len(alerts) > 0 and not(fatto):
        print("Moving ThingsController")
        alert_no+=len(alerts)
        fd.stop_app("dep1")
        fd.undeploy_component("dep1", "ThingsController")
        fog_node = "fog_1" #rnd.choice(["fog_1", "fog_2"])
        fd.deploy_component("dep1", "ThingsController", fog_node)
        fd.start_app("dep1")
        fatto = True
    alerts = []


print(str(alert_no) + " alerts were raised out of " + str(runs) + " runs.")
print(alert_no/(3*runs))

