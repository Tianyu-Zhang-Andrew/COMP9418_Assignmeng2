import csv

from solution import get_action


def convert_file_row_to_sensor_data(data_row):
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
        sensor_data[name] = data_row[i + 14]

    # Door sensor data
    for i in range(1, 12):
        name = "door_sensor" + str(i)
        sensor_data[name] = int(eval(data_row[i + 16]))

    # Time
    sensor_data['time'] = data_row[28]

    return sensor_data


def model_test(room_nums, file_name):
    full_data_file = open(file_name, "r", encoding="utf-8")
    reader = csv.reader(full_data_file)

    counts = {}
    for num in room_nums:
        counts[num] = {'non_empty_count': 0, 'false_off_count': 0, 'empty_count': 0, 'false_on_count': 0}

    cost = 0
    num = 0
    for row in reader:
        if num > 0:
            sensor_data = convert_file_row_to_sensor_data(row)
            actions = get_action(sensor_data)

            for num in room_nums:
                light = 'lights' + str(num)
                action = actions[light]

                if row[28 + num] == '0':
                    counts[num]['empty_count'] += 1
                    if action == "on":
                        counts[num]['false_on_count'] += 1

                if row[28 + num] != '0':
                    counts[num]['non_empty_count'] += 1
                    if action == "off":
                        counts[num]['false_off_count'] += 1

                if action == "on":
                    cost += 1
                else:
                    cost += 4 * int(row[28 + num])

        num += 1

    # for num in room_nums:
    #     print('Room', num, ':')
    #     print("Empty room:", counts[num]['empty_count'], ", Light on:", counts[num]['false_on_count'])
    #     print("Non empty room:", counts[num]['non_empty_count'], ", Light off:", counts[num]['false_off_count'])
    #     print()

    print("Cost:", cost)


model_test([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "data1.csv")
