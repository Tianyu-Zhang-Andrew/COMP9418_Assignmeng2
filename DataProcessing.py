import copy
import csv

import pandas as pd


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
        sensor_data[name] = int(eval(data_row[i + 10]))

    # Robot data
    for i in range(1, 3):
        name = "robot" + str(i)
        sensor_data[name] = eval(data_row[i + 14])

    # Door sensor data
    for i in range(1, 12):
        name = "door_sensor" + str(i)
        sensor_data[name] = int(eval(data_row[i + 16]))

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


def convert_file(file_name):
    global state
    full_data_file = open(file_name, "r", encoding="utf-8")
    reader = csv.reader(full_data_file)

    data = []

    row_number = 0
    for row in reader:
        if row_number > 0:
            converted_row = convert_row(row)
            data.append(converted_row)

            # Update the state of each room in this turn
            for i in range(1, 11):
                state["R" + str(i) + "_t-1"] = converted_row["R" + str(i) + "_t"]

        row_number += 1

    full_data_file.close()

    return pd.DataFrame(data)


