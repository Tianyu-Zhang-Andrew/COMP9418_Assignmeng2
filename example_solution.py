'''
COMP9418 Assignment 2
This file is the example code to show how the assignment will be tested.

Name:     zID:

Name:     zID:
'''

# Make division default to floating-point, saving confusion
from __future__ import division
from __future__ import print_function

# Allowed libraries
import numpy as np
import pandas as pd
import scipy as sp
import scipy.special
import heapq as pq
import matplotlib as mp
import matplotlib.pyplot as plt
import math
from itertools import product, combinations
from collections import OrderedDict as odict
import collections
from graphviz import Digraph, Graph
from tabulate import tabulate
import copy
import sys
import os
import datetime
import sklearn
import ast
import re
import pickle
import json

from DataProcessing import initialize_state
from Room1And2And7And8Model import get_room_1_room_2_room_7_room_8_model


state = initialize_state()
join_tree1278, bayesian_network_graph1278 = get_room_1_room_2_room_7_room_8_model("data1.csv")


def convert_sensor_data(sensor_data):
    global state

    # Convert door sensor data to "odd"/"even"/"zero"
    for i in range(1, 12):
        name = "door_sensor" + str(i)

        if sensor_data[name] is None:
            sensor_data[name] = None
        else:
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
        if sensor_data[name] is None:
            sensor_data[name] = None
        else:
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


def decide_action(prob_factor, sensor_data, room_num):
    for name in ["robot1", "robot2"]:
        if sensor_data[name][0] != "outside" and room_num == sensor_data[name][0]:

            if sensor_data[name][1] == 0:
                return 'off', 1, '0'
            elif sensor_data[name][1] == 1:
                return 'on', 1, '1'
            else:
                return 'on', 1, '>1'

    probs = [prob_factor['0'], prob_factor['1'], prob_factor['>1']]

    coef = {'r1': 2864/1938, 'r2': 4025/777, 'r7': 4401/401, 'r8': 1, 'c3': 3989/813}

    if prob_factor['0'] > 4 * coef[room_num] * (prob_factor['1'] + prob_factor['>1']):
        return 'off', max(probs), '0'
    elif prob_factor['>1'] > prob_factor['1']:
        return 'on', max(probs), '>1'
    else:
        return 'on', max(probs), '1'

    # if max(probs) == prob_factor['0']:
    #     if prob_factor['0'] > 4 * coef[room_num] * (prob_factor['1'] + prob_factor['>1']):
    #         return 'off', max(probs), '0'
    #     else:
    #         return 'on', max(probs), '0'
    #
    # elif max(probs) == prob_factor['1']:
    #     return 'on', max(probs), '1'
    #
    # else:
    #     return 'on', max(probs), '>1'


def generate_evidence(converted_sensor_data, bayesian_network):
    global state

    # Retrieve the last state of each room
    for i in range(1, 11):
        name = "R" + str(i) + "_t-1"
        converted_sensor_data[name] = state[name]

    # Retrieve the last state of corridor 3
    converted_sensor_data['C3_t-1'] = state['C3_t-1']

    # Use all sensor data, last room states and last corridor 3 state as evidence
    # Ignore the None reading of malfunctioned sensor
    evidence = {}
    for key in converted_sensor_data:
        if key in bayesian_network and converted_sensor_data[key] is not None:
            evidence[key] = converted_sensor_data[key]

    return evidence


def get_room_1278_actions(converted_sensor_data):
    global state

    evidence = generate_evidence(converted_sensor_data, bayesian_network_graph1278)

    join_tree1278.evidence(**evidence)
    join_tree1278.getMessages()

    action1, prob1, current_state1 = decide_action(join_tree1278.queryCluster('g', ('R1_t',)), converted_sensor_data,
                                                   'r1')
    action2, prob2, current_state2 = decide_action(join_tree1278.queryCluster('b', ('R2_t',)), converted_sensor_data,
                                                   'r2')
    action7, prob7, current_state7 = decide_action(join_tree1278.queryCluster('5', ('R7_t',)), converted_sensor_data,
                                                   'r7')
    action8, prob8, current_state8 = decide_action(join_tree1278.queryCluster('2', ('R8_t',)), converted_sensor_data,
                                                   'r8')

    # Update the state of each room
    state["R1_t-1"] = current_state1
    state["R2_t-1"] = current_state2
    state["R7_t-1"] = current_state7
    state["R7_t-1"] = current_state8

    # Update the state of corridor 3
    actionC3, probC3, current_stateC3 = decide_action(join_tree1278.queryCluster('8', ('C3_t',)), converted_sensor_data,
                                                      'c3')
    state["C3_t-1"] = current_stateC3

    join_tree1278.reset()

    return {'lights1': action1, 'lights2': action2, 'lights7': action7, 'lights8': action8}


def get_action(sensor_data):
    converted_sensor_data = convert_sensor_data(sensor_data)
    actions_dict = get_room_1278_actions(converted_sensor_data)

    return actions_dict


