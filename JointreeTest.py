import copy
import csv

from BayesNet import BayesNet
from DataProcessing import convert_file
from Graph import Graph
from JoinTree import JoinTree


def get_action(prob_factor, sensor_data, room_num):
    for name in ["robot1", "robot2"]:

        if sensor_data[name][0] != "outside" and room_num == int(sensor_data[name][0][1:]):
            if sensor_data[name][1] == 0:
                return 'off', 1, '0'
            elif sensor_data[name][1] == 1:
                return 'on', 1, '1'
            else:
                return 'on', 1, '>1'

    probs = [prob_factor['0'], prob_factor['1'], prob_factor['>1']]
    if max(probs) == prob_factor['0']:
        return 'off', max(probs), '0'
    elif max(probs) == prob_factor['1']:
        return 'on', max(probs), '1'
    else:
        return 'on', max(probs), '>1'


def initialize_state():
    # The initial number of detected people of each camera is set to 1
    initial_state = {}
    for i in range(1, 5):
        name = "Camera_sensor" + str(i)
        initial_state[name] = 1

    # The initial state of each room except room 3 is set to '0', room 3 is set to '>1'
    for i in range(1, 11):
        name = "R" + str(i) + "_t-1"
        if i == 3:
            initial_state[name] = '>1'
        else:
            initial_state[name] = '0'

    return initial_state


state = initialize_state()


def reset_state():
    global state
    state = initialize_state()


# Convert door sensor data from numerical numbers to "odd"/"even"/"zero"
# Convert camera data from numerical numbers to "increasing"/"decreasing"/"unchanged"/"zero"
# Retrieve the state of each room in the last term
def convert_sensor_data(sensor_data):
    global state

    # Convert door sensor data to "odd"/"even"/"zero"
    for i in range(1, 12):
        name = "door_sensor" + str(i)

        if sensor_data[name] % 2 == 0:
            if sensor_data[name] == 0:
                sensor_data[name] = "zero"
            else:
                sensor_data[name] = "even"
        else:
            sensor_data[name] = "odd"

    # Convert camera data to "increasing"/"decreasing"/"unchanged"/"zero"
    for i in range(1, 5):
        name = "Camera_sensor" + str(i)

        backup_sensor_data = copy.deepcopy(sensor_data)

        # Compare the number of people detected by each camera in this turn and the last turn
        # Convert the number of people detected by each camera to 'increasing'/"decreasing"/"unchanged"/"zero"
        if sensor_data[name] == 0:
            sensor_data[name] = "zero"
        elif sensor_data[name] > state[name]:
            sensor_data[name] = "increasing"
        elif sensor_data[name] == state[name]:
            sensor_data[name] = "unchanged"
        else:
            sensor_data[name] = "decreasing"

        # Update the detected people number of each camera
        state[name] = backup_sensor_data[name]

    # Retrieve the last state of each room
    for i in range(1, 11):
        name = "R" + str(i) + "_t-1"
        sensor_data[name] = state[name]

    return sensor_data


# Convert a row in the csv file into a dictionary
def convert_row(data_row):
    sensor_data = {}

    # Motion sensor data
    for i in range(1, 11):
        name = "Motion_Sensor" + str(i)
        sensor_data[name] = data_row[i]

    # Camera data
    for i in range(1, 5):
        name = "Camera_sensor" + str(i)
        sensor_data[name] = int(data_row[i + 10])

    # Robot data
    for i in range(1, 3):
        name = "robot" + str(i)
        sensor_data[name] = eval(data_row[i + 14])

    # Door sensor data
    for i in range(1, 12):
        name = "door_sensor" + str(i)
        sensor_data[name] = int(data_row[i + 16])

    # Time
    sensor_data['time'] = data_row[28]

    # Number of people in each room
    for i in range(1, 11):
        name = "R" + str(i) + "_t"

        if int(data_row[i + 28]) == 0:
            sensor_data[name] = '0'
        elif int(data_row[i + 28]) == 1:
            sensor_data[name] = '1'
        else:
            sensor_data[name] = '>1'

    # Number of people in corridor
    for i in range(1, 4):
        name = "C" + str(i) + "_t"
        sensor_data[name] = int(data_row[i + 38])

    # Number of people outside
    sensor_data['outside_t'] = int(data_row[42])

    # Convert some numerical data into categorical
    converted_data = convert_sensor_data(sensor_data)

    return converted_data


outcomeSpace = {
    "Motion_Sensor1": ('motion', 'no motion'),
    "Motion_Sensor2": ('motion', 'no motion'),
    "R1_t": ('0', '1', ">1"),
    "R2_t": ('0', '1', ">1"),
    "R1_t-1": ('0', '1', ">1"),
    "R2_t-1": ('0', '1', ">1"),
    "door_sensor1": ('odd', "even", "zero"),
    "door_sensor10": ('odd', "even", "zero"),
    "Camera_sensor1": ('increasing', "decreasing", "unchanged", "zero")
}

bayesian_network = Graph({
    "Camera_sensor1": [],
    "R1_t-1": ["Camera_sensor1", "door_sensor1", "R1_t"],
    "R1_t": ["Camera_sensor1", "Motion_Sensor1"],
    "door_sensor1": ["R1_t", "R2_t"],
    "R2_t-1": ["door_sensor1", "R2_t", "door_sensor10"],
    "R2_t": ["Motion_Sensor2"],
    "door_sensor10": ["R2_t"],
    "Motion_Sensor1": [],
    "Motion_Sensor2": []
})

join_tree = Graph({
    '1': ('2', '3'),
    '2': ('1',),
    '3': ('1', '4'),
    '4': ('3', '5', '6'),
    '5': ('4',),
    '6': ('4',)
})

S = {
    '12': ('R2_t',),
    '13': ('R2_t-1', 'D1_t'),
    '34': ('R1_t-1', 'D1_t'),
    '45': ('R1_t',),
    '46': ('R1_t-1', 'R1_t')
}

C = {
    '1': ('door_sensor1', 'R2_t-1', 'R2_t', 'door_sensor10'),
    '2': ('Motion_Sensor2', 'R2_t'),
    '3': ('R1_t-1', 'R2_t-1', 'door_sensor1'),
    '4': ('R1_t', 'R1_t-1', 'door_sensor1'),
    '5': ('Motion_Sensor1', 'R1_t'),
    '6': ('Camera_sensor1', 'R1_t-1', 'R1_t')
}

data = convert_file("data1.csv")

BN = BayesNet(bayesian_network, outcomeSpace=outcomeSpace)
BN.learnParameters(data)
print(BN.factors['Motion_Sensor1'])
# jt = JoinTree(join_tree, C, S, outcomeSpace)
# jt.distribute_factors(BN.factors.values())

# full_data_file = open("data1.csv", "r", encoding="utf-8")
# reader = csv.reader(full_data_file)
#
# non_empty_count = 0
# false_off_count = 0
# empty_count = 0
# false_on_count = 0
# num = 0
# for row in reader:
#     if num > 0:
#         converted_data = convert_row(row)
#
#         evidence = {}
#         for key in converted_data:
#             if key in BN.graph:
#                 evidence[key] = converted_data[key]
#
#         jt.evidence(**evidence)
#         jt.getMessages()
#
#         action1, prob1, current_state1 = get_action(jt.queryCluster('6', ('R1_t',)), converted_data, 1)
#         action2, prob2, current_state2 = get_action(jt.queryCluster('1', ('R2_t',)), converted_data, 1)
#
#         state["R1_t-1"] = current_state1
#         state["R2_t-1"] = current_state2
#
#         # if action1 == "on":
#         #     total_count += 1
#         #
#         #     if converted_data["R1_t"] == '0':
#         #         error_count += 1
#
#         if converted_data["R2_t"] == '0':
#             empty_count += 1
#             if action2 == "on":
#                 false_on_count += 1
#
#         if converted_data["R2_t"] != '0':
#             non_empty_count += 1
#             if action2 == "off":
#                 false_off_count += 1
#
#         jt.reset()
#
#     num += 1
#
# print("Empty room:", empty_count, ", Light on:", false_on_count)
# print("Non empty room:", non_empty_count, ", Light off:", false_off_count)