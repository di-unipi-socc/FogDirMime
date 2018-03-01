from fog_director import *

fd = FogDirSim()

fd.add_thing("fire0", "fire")
fd.add_thing("thermostate0", "thermostate")
fd.add_thing("water0", "water")
fd.add_thing("video0", "video")

#fog_1
cpu = ProbabilityDistribution([0.8, 0.2],[2.0, 1.0])
ram = ProbabilityDistribution([0.8, 0.10, 0.10],[2.0, 1.0, 0.5])
hdd = ProbabilityDistribution([0.8, 0.10, 0.10],[16.0, 8.0, 4.0])
hw = HardwareResources(ram, hdd, cpu)
fog_1 = Node("fog_1", hw, ["linux", "php", "sql"])
fd.add_node(fog_1)

#fog_2
cpu2 = ProbabilityDistribution([0.9, 0.1],[2.0, 1.0])
ram2 = ProbabilityDistribution([0.6, 0.20, 0.1, 0.1],[4.0, 3.0, 2.0, 1.0])
hdd2 = ProbabilityDistribution([0.8, 0.10, 0.10],[28.0, 25.0, 20.0])

hw2 = HardwareResources(ram2, hdd2, cpu2)
fog_2 = Node("fog_2", hw2, ["linux", "php"])
fd.add_node(fog_2)

#fog3
cpu3 = ProbabilityDistribution([0.5, 0.3, 0.2],[4.0, 3.0, 2.0])
hdd3 = ProbabilityDistribution([1.0],[50.0])
ram3 = ProbabilityDistribution([0.8, 0.10, 0.10],[4.0, 3.0, 2.0])

hw3 = HardwareResources(ram3, hdd3, cpu3)
fog_3 = Node("fog_3", hw3, ["linux", "sql"])
fd.add_node(fog_3)

# #cloud1
# hdd_c1 = ProbabilityDistribution([1.0],[160])
# ram_c1 = ProbabilityDistribution([1.0],[16])
# cpu_c1 = ProbabilityDistribution([1.0],[8])
# hw_c1 = HardwareResources(ram_c1, hdd_c1, cpu_c1)
# cloud_1 = Node("cloud_1", hw_c1, ["linux", "sql"])
# fd.add_node(cloud_1)

# #cloud2
# hdd_c2 = ProbabilityDistribution([1.0],[160])
# ram_c2 = ProbabilityDistribution([1.0],[16])
# cpu_c2 = ProbabilityDistribution([1.0],[8])
# hw_c2 = HardwareResources(ram_c2, hdd_c2, cpu_c2)
# cloud_2 = Node("cloud_1", hw_c2, ["linux", "sql"])
# fd.add_node(cloud_2)

#fog_1 - fog_2
b_f1_f2 = ProbabilityDistribution([0.9, 0.1], [32.0, 16.0])
b_f2_f1 = ProbabilityDistribution([0.9, 0.1], [32.0, 16.0])
l_f1_f2 = ProbabilityDistribution([1.0], [15.0])
q_f1_f2 = QoSProfile(b_f1_f2, b_f2_f1, l_f1_f2)
q_f1_f2.sample_qos()

fd.add_link(Link("fog_1", "fog_2", q_f1_f2))

#fog_2 - fog_3
b_f2_f3 = ProbabilityDistribution([0.8, 0.2], [6, 2.0])
b_f3_f2 = ProbabilityDistribution([0.8, 0.2], [60.0, 35.0])
l_f2_f3 = ProbabilityDistribution([1.0], [60.0])
q_f2_f3 = QoSProfile(b_f2_f3, b_f3_f2, l_f2_f3)
q_f2_f3.sample_qos()

fd.add_link(Link("fog_2", "fog_3", q_f2_f3))


#fog_1 - fog_3
b_f1_f3 = ProbabilityDistribution([0.9, 0.1], [32.0, 16.0])
b_f3_f1 = ProbabilityDistribution([0.9, 0.1], [32.0, 16.0])
l_f1_f3 = ProbabilityDistribution([1.0], [15.0])
q_f1_f3 = QoSProfile(b_f1_f3, b_f3_f1, l_f1_f3)
q_f1_f3.sample_qos()

fd.add_link(Link("fog_1", "fog_3", q_f1_f3))

# #fog to things
# b_ = ProbabilityDistribution([0.9, 0.1], [32.0, 16.0])
# b_f3_f1 = ProbabilityDistribution([0.9, 0.1], [32.0, 16.0])
# l_f1_f3 = ProbabilityDistribution([1.0], [15.0])

# fd.add_link(Link("fog_1", "fire0", q) )
# fd.add_link(Link("fog_1", "thermostate0", q) )
# fd.add_link(Link("fog_2", "fire0", q) )
# fd.add_link(Link("fog_2", "thermostate0", q) )

print(fd.infrastructure.links)

fd.sample_state()


filename = "app_1.json"
app = {}
with open(filename) as file_object:
    app = json.load(file_object) 
print(app)
fd.publish_app("app1", app)
fd.new_deployment("dep1", "app1")
fd.deploy_component("dep1", "SmartBuilding", "fog_1")
fd.bind_thing("dep1", 0, "thermostate0")  
fd.bind_thing("dep1", 1, "fire0") 
fd.bind_thing("dep1", 2, "video0") 
fd.start_app("dep1")

runs = 10000

alert_no = 0
res_alert = 0
c2c_alert = 0
for i in range(0, runs):
    fatto = False
    alerts=fd.get_alert("dep1")
    print("****" + str(alerts))
    for alert in alerts:
        if alert['alert_type'] == 'c2c':
            c2c_alert = c2c_alert + 1
        elif alert['alert_type'] == 'resources':
            res_alert = res_alert + 1
    alert_no+=len(alerts)
    #print(alert_no)
    # if alerts is not None and len(alerts) > 0 and not(fatto):
    #     print("Moving ThingsController")
    #     alert_no+=len(alerts)
    #     fd.stop_app("dep1")
    #     fd.undeploy_component("dep1", "ThingsController")
    #     fog_node = "fog_1" #rnd.choice(["fog_1", "fog_2"])
    #     fd.deploy_component("dep1", "ThingsController", fog_node)
    #     fd.start_app("dep1")
    #     fatto = True
    # alerts = []

print(res_alert)
print(c2c_alert)
print(str(alert_no) + " alerts were raised out of " + str(runs) + " runs.")
print(alert_no/(3*runs))

