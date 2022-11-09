import copy
import csv

from DataProcessing import initialize_state
from Room1And2Model import get_room_1_room_2_model


state = initialize_state()


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

    return sensor_data


def convert_file_row_to_sensor_data(data_row):
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

    # Convert some numerical data into categorical
    final_sensor_data = convert_sensor_data(sensor_data)

    return final_sensor_data


join_tree, bayesian_network_graph = get_room_1_room_2_model("data1.csv")

full_data_file = open("data1.csv", "r", encoding="utf-8")
reader = csv.reader(full_data_file)

non_empty_count = 0
false_off_count = 0
empty_count = 0
false_on_count = 0

num = 0
for row in reader:
    if num > 0:
        converted_sensor_data = convert_file_row_to_sensor_data(row)

        # Retrieve the last state of each room
        for i in range(1, 11):
            name = "R" + str(i) + "_t-1"
            converted_sensor_data[name] = state[name]

        # Use all data from sensor and last room state as evidence
        evidence = {}
        for key in converted_sensor_data:
            if key in bayesian_network_graph:
                evidence[key] = converted_sensor_data[key]

        join_tree.evidence(**evidence)
        join_tree.getMessages()

        action1, prob1, current_state1 = get_action(join_tree.queryCluster('6', ('R1_t',)), converted_sensor_data, 1)
        action2, prob2, current_state2 = get_action(join_tree.queryCluster('1', ('R2_t',)), converted_sensor_data, 2)

        # Update the state of each room
        state["R1_t-1"] = current_state1
        state["R2_t-1"] = current_state2

        if row[30] == '0':
            empty_count += 1
            if action2 == "on":
                false_on_count += 1

        if row[30] != '0':
            non_empty_count += 1
            if action2 == "off":
                false_off_count += 1

        join_tree.reset()

    num += 1

print("Empty room:", empty_count, ", Light on:", false_on_count)
print("Non empty room:", non_empty_count, ", Light off:", false_off_count)
