from fog_director import *

fd = FogDirSim()

fd.add_thing("fire0", "fire")
fd.add_thing("thermostat0", "thermostat")
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
l_f2_f3 = ProbabilityDistribution([0.7, 0.3], [25.0, 30.0])
q_f2_f3 = QoSProfile(b_f2_f3, b_f3_f2, l_f2_f3)
q_f2_f3.sample_qos()

fd.add_link(Link("fog_2", "fog_3", q_f2_f3))


#fog_1 - fog_3
b_f1_f3 = ProbabilityDistribution([0.8, 0.2], [6.0, 2.0])
b_f3_f1 = ProbabilityDistribution([0.9, 0.1], [60.0, 35.0])
l_f1_f3 = ProbabilityDistribution([0.7, 0.2, 0.1], [25.0, 30.0, 40.0])
q_f1_f3 = QoSProfile(b_f1_f3, b_f3_f1, l_f1_f3)
q_f1_f3.sample_qos()

fd.add_link(Link("fog_1", "fog_3", q_f1_f3))

#fog-to-things
b_thing = ProbabilityDistribution([1.0], [100.0])
l_thing = ProbabilityDistribution([1.0], [0.0])
q_thing = QoSProfile(b_thing, b_thing, l_thing)
q_thing.sample_qos()

fd.add_link(Link("thermostat0", "fog_1", q_thing))
fd.add_link(Link("fire0", "fog_1", q_thing))
fd.add_link(Link("video0", "fog_1", q_f1_f2))

fd.add_link(Link("thermostat0", "fog_2", q_f1_f2))
fd.add_link(Link("fire0", "fog_2", q_f1_f2))
fd.add_link(Link("video0", "fog_2", q_thing))

fd.add_link(Link("thermostat0", "fog_3", q_f1_f3))
fd.add_link(Link("fire0", "fog_3", q_f1_f3))
fd.add_link(Link("video0", "fog_3", q_f2_f3))

fd.sample_state()


filename = "app_1.json"
app = {}
with open(filename) as file_object:
    app = json.load(file_object) 
print(app)
fd.publish_app("app1", app)
fd.new_deployment("dep1", "app1")
while fd.deploy_component("dep1", "SmartBuilding", "fog_1") != 1 :
    print("trying deployment")
fd.bind_thing("dep1", 0, "thermostat0")  
fd.bind_thing("dep1", 1, "fire0") 
fd.bind_thing("dep1", 2, "video0") 
fd.start_app("dep1")

runs = 1000

alert_no = 0
res_alert = 0
c2c_alert = 0
c2t_alert = 0
migrations = 0


nodes = ["fog_1", "fog_2", "fog_3"]
major_failure = 0

for i in range(0, runs):
    
    alerts=fd.get_alert("dep1")
    print("****" + str(alerts))
    if alerts:
        for alert in alerts:
            if alert['alert_type'] == 'c2t':
                c2t_alert = c2t_alert + 1
            elif alert['alert_type'] == 'c2c':
                c2c_alert = c2c_alert + 1
            elif alert['alert_type'] == 'resources':
                res_alert = res_alert + 1
        alert_no+=len(alerts)
    print(alert_no)

    if alerts is not None and len(alerts) > 0:
        migrations += 1
        fd.stop_app("dep1")
        fd.undeploy_component("dep1", "SmartBuilding")
        if(nodes):
            fog_node = nodes.pop()
            while fd.deploy_component("dep1", "SmartBuilding", fog_node) != 1:
                continue
            fd.start_app("dep1")
        else:
            print("Major failure")
            major_failure+=1
            #fd.stop_app("dep1")
            nodes = ["fog_1", "fog_2", "fog_3"]
            fd.undeploy_component("dep1", "SmartBuilding")
            while fd.deploy_component("dep1", "SmartBuilding", "fog_1") != 1 :
                print("restarting deplo")
            fd.start_app("dep1")
            

    alerts = []

print("Resource alerts", res_alert)
print("Things alerts", c2t_alert)
print(str(alert_no) + " alerts were raised out of " + str(runs) + " runs.")


print(major_failure)


    # if alerts is not None and len(alerts) > 0 and not(fatto):
    #     print("Moving ThingsController")
    #     alert_no+=len(alerts)
    #     fd.stop_app("dep1")
    #     fd.undeploy_component("dep1", "SmartBuilding")
    #     fog_node = "fog_2" #rnd.choice(["fog_1", "fog_2"])
    #     fd.deploy_component("dep1", "SmartBuilding", fog_node)
    #     fd.start_app("dep1")
    #     fatto = True