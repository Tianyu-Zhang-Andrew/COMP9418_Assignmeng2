import csv

full_data_file = open("data2.csv", "r", encoding="utf-8")
reader = csv.reader(full_data_file)

global titles

row_number = 0
data = []
count = 0
for row in reader:
    if row_number > 0:
        data.append(row)

        if eval(row[17]) % 2 != 0 and eval(row[26]) % 2 != 0:
            count += 1

    else:
        titles = row

    row_number += 1

full_data_file.close()

print(count)

# count = 0
# for row in data:
#     if int(row[39]) != 0:
#         count += 1
#
# print(titles[39], count)



# Robot
# name_index_dict = {}
# for i in range(1, len(titles)):
#     name_index_dict[titles[i]] = i
#
# robot_dict = {}
# for i in [15, 16]:
#     robot_dict[titles[i]] = {}
#     correct_count = 0
#     for row in data:
#         location_name = eval(row[i])[0]
#         index = name_index_dict[location_name]
#
#         actual_number = int(row[index])
#         robot_count_number = int(eval(row[i])[1])
#
#         if actual_number == robot_count_number:
#             correct_count += 1
#
#     robot_dict[titles[i]]["Count correct"] = correct_count
#
# print(robot_dict)

# correct_count = 0
# total_count = 0
# for row in data:
#     if float(row[14]) == 0:
#         total_count += 1
#
#         if float(row[41]) == 0:
#             correct_count += 1
# #
# #     if float(row[14]) == float(row[41]):
# #         correct_count += 1
# #
# print(titles[14], titles[41])
# print(correct_count, total_count)

# Camera~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# room_index = [29, 32, 36, 41]
# camera_index = [11, 12, 13, 14]
# cam_dict = {}
#
# for j in range(0, len(camera_index)):
#     cam_dict[titles[camera_index[j]]] = {}
#
#     correct_diff_count = 0
#     correct_change_count = 0
#     for i in range(1, len(data)):
#         camera_diff = float(data[i][camera_index[j]]) - float(data[i - 1][camera_index[j]])
#         actual_diff = float(data[i][room_index[j]]) - float(data[i - 1][room_index[j]])
#
#         if (camera_diff * actual_diff > 0) or (camera_diff == 0 and actual_diff == 0):
#             correct_change_count += 1
#
#         if camera_diff == actual_diff:
#             correct_diff_count += 1
#
#     cam_dict[titles[camera_index[j]]]["Correct difference count"] = correct_diff_count
#     cam_dict[titles[camera_index[j]]]["Correct change count"] = correct_change_count
#
#
# for key in cam_dict:
#     print(key, cam_dict[key])

# Motion sensor~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# motion_sensor_dict = {}
# for i in range(1, 11):
#     motion_sensor_dict[titles[i]] = {}
#
#     error_count = 0
#     motion_count = 0
#     for row in data:
#         if int(row[28 + i]) == 0:
#             motion_count += 1
#
#             if row[i] == "motion":
#                 error_count += 1
#
#     motion_sensor_dict[titles[i]]["Total motion count"] = motion_count
#     motion_sensor_dict[titles[i]]["Error count"] = error_count
#
# for key in motion_sensor_dict:
#     print(key, motion_sensor_dict[key])
