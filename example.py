from fog_director import *

fd = FogDirSim()

fd.add_thing("fire0", "fire")
fd.add_thing("thermostat0", "thermostat")
fd.add_thing("video0", "video")

fd.add_thing("fire1", "fire")
fd.add_thing("thermostat1", "thermostat")


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
fd.add_link(Link("thermostat1", "fog_1", q_f1_f2))
fd.add_link(Link("fire1", "fog_1", q_f1_f2))
fd.add_link(Link("video0", "fog_1", q_f1_f2))

fd.add_link(Link("thermostat0", "fog_2", q_f1_f2))
fd.add_link(Link("fire0", "fog_2", q_f1_f2))
fd.add_link(Link("thermostat1", "fog_2", q_thing))
fd.add_link(Link("fire1", "fog_2", q_thing))
fd.add_link(Link("video0", "fog_2", q_thing))

fd.add_link(Link("thermostat0", "fog_3", q_f1_f3))
fd.add_link(Link("fire0", "fog_3", q_f1_f3))
fd.add_link(Link("video0", "fog_3", q_f2_f3))
fd.add_link(Link("thermostat1", "fog_3", q_f2_f3))
fd.add_link(Link("fire1", "fog_3", q_f2_f3))

fd.sample_state()


filename = "app_1.json"
app = {}
with open(filename) as file_object:
    app = json.load(file_object) 
print(app)

moved1 = False
moved2 = False

#publish the application
fd.publish_app("app1", app)

# dep1 manages the common parts of the building
fd.new_deployment("dep1", "app1")
<<<<<<< HEAD
while fd.deploy_component("dep1", "SmartBuild", "fog_1") != 1 :
    print("*** Cannot deploy to home router. ***")
=======
while fd.deploy_component("dep1", "SmartBuild", "fog_2") != 1 :
    print("*** Cannot deploy to the building switch. ***")
>>>>>>> 3d59126960111ba1f7033e60cf369b4af515875d
fd.bind_thing("dep1", 0, "thermostat1")  
fd.bind_thing("dep1", 1, "fire1") 
fd.bind_thing("dep1", 2, "video0") 
fd.start_app("dep1")

#dep 2 manages the house of the owner of fog1
fd.new_deployment("dep2", "app1")
<<<<<<< HEAD
while fd.deploy_component("dep2", "SmartBuild", "fog_2") != 1 :
    print("Deploying SmartBuild to home router...")
=======
while fd.deploy_component("dep2", "SmartBuild", "fog_1") != 1 :
    print("*** Cannot deploy to the home router. ***")
>>>>>>> 3d59126960111ba1f7033e60cf369b4af515875d
fd.bind_thing("dep2", 0, "thermostat0")  
fd.bind_thing("dep2", 1, "fire0") 
fd.bind_thing("dep2", 2, "video0") 
fd.start_app("dep2")

<<<<<<< HEAD
runs = 1000
=======

runs = 10000
>>>>>>> 3d59126960111ba1f7033e60cf369b4af515875d

alert_no = 0
res_alert1 = 0
c2c_alert1 = 0
c2t_alert1 = 0
migrations1 = 0

res_alert2 = 0
c2c_alert2 = 0
c2t_alert2 = 0
migrations2 = 0


<<<<<<< HEAD
moved1=False
moved2=False
=======

>>>>>>> 3d59126960111ba1f7033e60cf369b4af515875d
for i in range(0, runs):
    
    alerts1=fd.get_alert("dep1")
    alerts2=fd.get_alert("dep2")
<<<<<<< HEAD
    print("****" + str(alerts1))
    print("****" + str(alerts2))
=======

>>>>>>> 3d59126960111ba1f7033e60cf369b4af515875d
    if alerts1:
        for alert in alerts1:
            if alert['alert_type'] == 'c2t':
                c2t_alert1 = c2t_alert1 + 1
            elif alert['alert_type'] == 'c2c':
                c2c_alert1 = c2c_alert1 + 1
            elif alert['alert_type'] == 'resources':
                res_alert1 = res_alert1 + 1
        alert_no+=len(alerts1)
    if alerts2:
        for alert in alerts2:
            if alert['alert_type'] == 'c2t':
                c2t_alert2 = c2t_alert2 + 1
            elif alert['alert_type'] == 'c2c':
                c2c_alert2 = c2c_alert2 + 1
            elif alert['alert_type'] == 'resources':
                res_alert2 = res_alert2 + 1
        alert_no+=len(alerts2)

    for alert in alerts1:
<<<<<<< HEAD
        if alert['alert_type'] == 'resources' and not moved1:
=======
        if alert['alert_type'] == 'resources' and not(moved1):
>>>>>>> 3d59126960111ba1f7033e60cf369b4af515875d
            migrations1 += 1
            moved1=True
            fd.stop_app("dep1")
            fd.undeploy_component("dep1", "SmartBuild")
<<<<<<< HEAD
            while fd.deploy_component("dep1", "SmartBuild", "fog_2") != 1:
=======
            while fd.deploy_component("dep1", "SmartBuild", "fog_3") != 1:
>>>>>>> 3d59126960111ba1f7033e60cf369b4af515875d
                continue
            fd.start_app("dep1")
            moved1 = True
            break

    for alert in alerts2:
        if alert['alert_type'] == 'resources' and not moved2:
            migrations2 += 1
            moved2=True
            fd.stop_app("dep2")
            fd.undeploy_component("dep2", "SmartBuild")
<<<<<<< HEAD
            while fd.deploy_component("dep2", "SmartBuild", "fog_3") != 1:
=======
            if not(moved2):
                fog_node = "fog_2"
            else:
                fog_node = "fog_1"    
            while fd.deploy_component("dep2", "SmartBuild", fog_node) != 1:
>>>>>>> 3d59126960111ba1f7033e60cf369b4af515875d
                continue
            fd.start_app("dep2")
            moved2 = not(moved2)
            break
<<<<<<< HEAD
    
    alerts2 = []
=======

>>>>>>> 3d59126960111ba1f7033e60cf369b4af515875d
    alerts1 = []
    alerts2 = []


print("Simulating management plan for", runs, "epochs.")
print("*** RESULTS ***")
print("*** dep1 ***")
print("\t Resource alerts:", res_alert1)
print("\t A2T alerts:", c2t_alert1)
print("\t Migrations:", migrations1)
print()
print("*** dep2 ***")
print("\t Resource alerts:", res_alert2)
print("\t A2T alerts:", c2t_alert2)
print("\t Migrations:", migrations2)
