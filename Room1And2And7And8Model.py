from BayesNet import BayesNet
from DataProcessing import convert_file
from Graph import Graph
from JoinTree import JoinTree

outcomeSpace = {
    "Motion_Sensor1": ('motion', 'no motion'),
    "Motion_Sensor2": ('motion', 'no motion'),
    "R1_t": ('0', '1', ">1"),
    "R2_t": ('0', '1', ">1"),
    "R1_t-1": ('0', '1', ">1"),
    "R2_t-1": ('0', '1', ">1"),
    "door_sensor1": ('odd', "even", "zero"),
    "door_sensor10": ('odd', "even", "zero"),
    "Camera_sensor1": ('increasing', "decreasing", "unchanged", "zero"),
    "Motion_Sensor7": ('motion', 'no motion'),
    "Motion_Sensor8": ('motion', 'no motion'),
    "R7_t": ('0', '1', ">1"),
    "R8_t": ('0', '1', ">1"),
    "R7_t-1": ('0', '1', ">1"),
    "R8_t-1": ('0', '1', ">1"),
    "door_sensor8": ('odd', "even", "zero"),
    "door_sensor9": ('odd', "even", "zero"),
    "Camera_sensor3": ('increasing', "decreasing", "unchanged", "zero"),
    "C3_t-1": ('0', '1', ">1"),
    "C3_t": ('0', '1', ">1"),
    "Camera_sensor4": ('increasing', "decreasing", "unchanged", "zero")
}

bayesian_network = Graph({
    "Camera_sensor1": [],
    "R1_t-1": ["Camera_sensor1", "door_sensor1", "R1_t"],
    "R1_t": ["Camera_sensor1", "Motion_Sensor1"],
    "door_sensor1": ["R1_t", "R2_t"],
    "R2_t-1": ["door_sensor1", "R2_t", "door_sensor10"],
    "R2_t": ["Motion_Sensor2"],
    "door_sensor10": ["R2_t", "C3_t"],
    "Motion_Sensor1": [],
    "Motion_Sensor2": [],
    "Camera_sensor3": [],
    "R8_t-1": ["Camera_sensor3", "door_sensor8", "R8_t"],
    "R8_t": ["Camera_sensor3", "Motion_Sensor8"],
    "door_sensor8": ["R8_t", "R7_t"],
    "R7_t-1": ["door_sensor8", "R7_t", "door_sensor9"],
    "R7_t": ["Motion_Sensor7"],
    "door_sensor9": ["R7_t", "C3_t"],
    "Motion_Sensor7": [],
    "Motion_Sensor8": [],
    "C3_t-1": ["door_sensor9", "door_sensor10", "C3_t", "Camera_sensor4"],
    "C3_t": ["Camera_sensor4"],
    "Camera_sensor4": []
})

join_tree = Graph({
    '1': ('2',),
    '2': ('1', '3'),
    '3': ('2', '4'),
    '4': ('3', '5'),
    '5': ('4', '6', '7'),
    '6': ('5',),
    '7': ('5', '8'),
    '8': ('7', '9', 'a'),
    '9': ('8',),
    'a': ('8', 'b'),
    'b': ('a', 'c', 'd'),
    'c': ('b',),
    'd': ('b', 'e'),
    'e': ('d', 'f', 'g'),
    'f': ('e',),
    'g': ('e',)
})

S = {
    '12': ('R8_t',),
    '23': ('R8_t-1', 'R8_t'),
    '34': ('R8_t-1', 'door_sensor8'),
    '45': ('R7_t-1', 'door_sensor8'),
    '56': ('R7_t',),
    '57': ('door_sensor9', 'R7_t-1'),
    '78': ('C3_t-1', 'door_sensor9'),
    '89': ('C3_t-1', 'C3_t'),
    '8a': ('door_sensor10', 'C3_t-1'),
    'ab': ('R2_t-1', 'door_sensor10'),
    'bc': ('R2_t',),
    'bd': ('R2_t-1', 'door_sensor1'),
    'de': ('R1_t-1', 'door_sensor1'),
    'eg': ('R1_t-1', 'R1_t'),
    'ef': ('R1_t',)
}

C = {
    '1': ('Motion_Sensor8', 'R8_t'),
    '2': ('Camera_sensor3', 'R8_t', 'R8_t-1'),
    '3': ('R8_t', 'R8_t-1', 'door_sensor8'),
    '4': ('R8_t-1', 'R7_t-1', 'door_sensor8'),
    '5': ('door_sensor9', 'R7_t-1', 'R7_t', 'door_sensor8'),
    '6': ('Motion_Sensor7', 'R7_t'),
    '7': ('C3_t-1', 'door_sensor9', 'R7_t-1'),
    '8': ('door_sensor10', 'C3_t-1', 'C3_t', 'door_sensor9'),
    '9': ('Camera_sensor4', 'C3_t-1', 'C3_t'),
    'a': ('R2_t-1', 'C3_t-1', 'door_sensor10'),
    'b': ('door_sensor1', 'R2_t-1', 'R2_t', 'door_sensor10'),
    'c': ('R2_t', 'Motion_Sensor2'),
    'd': ('R1_t-1', 'R2_t-1', 'door_sensor1'),
    'e': ('R1_t-1', 'R1_t', 'door_sensor1'),
    'f': ('Motion_Sensor1', 'R1_t'),
    'g': ('Camera_sensor1', 'R1_t-1', 'R1_t')
}


def learn_factor(training_file):
    data = convert_file(training_file)
    bayesian_net = BayesNet(bayesian_network, outcomeSpace=outcomeSpace)
    bayesian_net.learnParameters(data)
    return bayesian_net.factors


def get_room_1_room_2_room_7_room_8_model(training_file):
    factor = learn_factor(training_file)
    jt = JoinTree(join_tree, C, S, outcomeSpace)
    jt.distribute_factors(factor.values())
    return jt, bayesian_network
