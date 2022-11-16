import csv

full_data_file = open("Combine.csv", "r", encoding="utf-8")
reader = csv.reader(full_data_file)

global titles

row_number = 0
data = []
for row in reader:
    if row_number > 0:
        data.append(row)
    else:
        titles = row

    row_number += 1

full_data_file.close()

# # Robot
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

# # Camera~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# room_index = [29, 32, 36, 41]
# camera_index = [11, 12, 13, 14]
# cam_dict = {}
#
# # Camera motion
# for j in range(0, len(camera_index)):
#     cam_dict[titles[camera_index[j]]] = {}
# 
#     motion_detect = 0
#     non_motion_detect = 0
#     motion_error = 0
#     non_motion_error = 0
#     for i in range(1, len(data)):
#         if float(data[i][camera_index[j]]) != 0:
#             motion_detect += 1
# 
#             if float(data[i][room_index[j]]) == 0:
#                 motion_error += 1
# 
#         else:
#             non_motion_detect += 1
# 
#             if float(data[i][room_index[j]]) != 0:
#                 non_motion_error += 1
# 
#     cam_dict[titles[camera_index[j]]]["True motion"] = (motion_detect - motion_error) / motion_detect
#     cam_dict[titles[camera_index[j]]]["False motion"] = motion_error / motion_detect
#     cam_dict[titles[camera_index[j]]]["True non motion"] = (non_motion_detect - non_motion_error) / non_motion_detect
#     cam_dict[titles[camera_index[j]]]["False non motion"] = non_motion_error / non_motion_detect
# 
# for key in cam_dict:
#     print(key, cam_dict[key])
#
# # Camera count, difference and trend
# for j in range(0, len(camera_index)):
#     cam_dict[titles[camera_index[j]]] = {}
#
#     correct_diff_count = 0
#     correct_trend_count = 0
#     correct_count = 0
#
#     total_diff = 0
#     total_trend = 0
#     total_count = 0
#     for i in range(0, len(data)):
#
#         total_count += 1
#         if float(data[i][camera_index[j]]) == float(data[i][room_index[j]]):
#             correct_count += 1
#
#         if i >= 1:
#             camera_diff = float(data[i][camera_index[j]]) - float(data[i - 1][camera_index[j]])
#             actual_diff = float(data[i][room_index[j]]) - float(data[i - 1][room_index[j]])
#
#             total_trend += 1
#             total_diff += 1
#
#             if (camera_diff * actual_diff > 0) or (camera_diff == 0 and actual_diff == 0):
#                 correct_trend_count += 1
#
#             if camera_diff == actual_diff:
#                 correct_diff_count += 1
#
#     cam_dict[titles[camera_index[j]]]["Correct difference"] = correct_diff_count / total_diff
#     cam_dict[titles[camera_index[j]]]["Correct trend"] = correct_trend_count / total_trend
#     cam_dict[titles[camera_index[j]]]["Correct count"] = correct_count / total_count
#
# for key in cam_dict:
#     print(key, cam_dict[key])

# # Motion sensor~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# motion_sensor_dict = {}
# for i in range(1, 11):
#     motion_sensor_dict[titles[i]] = {}
#
#     motion_detect = 0
#     non_motion_detect = 0
#     motion_error = 0
#     non_motion_error = 0
#     for row in data:
#         if row[i] == "motion":
#             motion_detect += 1
#
#             if int(row[28 + i]) == 0:
#                 motion_error += 1
#         else:
#             non_motion_detect += 1
#
#             if int(row[28 + i]) != 0:
#                 non_motion_error += 1
#
#     motion_sensor_dict[titles[i]]["True motion"] = (motion_detect - motion_error) / motion_detect
#     motion_sensor_dict[titles[i]]["False motion"] = motion_error / motion_detect
#     motion_sensor_dict[titles[i]]["True non motion"] = (non_motion_detect - non_motion_error) / non_motion_detect
#     motion_sensor_dict[titles[i]]["False non motion"] = non_motion_error / non_motion_detect
#
# for key in motion_sensor_dict:
#     print(key, motion_sensor_dict[key])
