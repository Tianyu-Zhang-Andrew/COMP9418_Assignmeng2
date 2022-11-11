from BayesNet import BayesNet
from DataProcessing import convert_file
from Graph import Graph
from JoinTree import JoinTree

outcomeSpace = {
    "Motion_Sensor4": ('motion', 'no motion'),
    "Motion_Sensor5": ('motion', 'no motion'),
    "Motion_Sensor6": ('motion', 'no motion'),
    "Camera_sensor2": ('increasing', "decreasing", "unchanged", "zero"),
    "R4_t": ('0', '1', ">1"),
    "R5_t": ('0', '1', ">1"),
    "R6_t": ('0', '1', ">1"),
    "R4_t-1": ('0', '1', ">1"),
    "R5_t-1": ('0', '1', ">1"),
    "R6_t-1": ('0', '1', ">1"),
    "door_sensor3": ('odd', "even", "zero"),
    "door_sensor4": ('odd', "even", "zero"),
    "door_sensor5": ('odd', "even", "zero")
}

bayesian_network = Graph({
    "Motion_Sensor4": [],
    "Motion_Sensor5": [],
    "Motion_Sensor6": [],
    "Camera_sensor2": [],
    "R4_t": ["Motion_Sensor4", "Camera_sensor2", "door_sensor3"],
    "R5_t": ["Motion_Sensor5"],
    "R6_t": ["Motion_Sensor6"],
    "R4_t-1": ["door_sensor3", "R4_t", "Camera_sensor2", "door_sensor4"],
    "R5_t-1": ["door_sensor4", "R5_t", "door_sensor5"],
    "R6_t-1": ["door_sensor5", "R6_t"],
    "door_sensor3": [],
    "door_sensor4": ["R4_t", "R5_t"],
    "door_sensor5": ["R5_t", "R6_t"]
})

join_tree = Graph({
    '1': ('2',),
    '2': ('1', '3', '4'),
    '3': ('2',),
    '4': ('2', '6'),
    '5': ('6',),
    '6': ('4', '5', '7'),
    '7': ('6', '8'),
    '8': ('7', '9'),
    '9': ('8',)
})

S = {
    '12': ('R4_t',),
    '23': ('R4_t-1', 'R4_t'),
    '24': ('R4_t-1', 'door_sensor4'),
    '46': ('R5_t-1', 'door_sensor4'),
    '56': ('R5_t',),
    '67': ('R5_t-1', 'door_sensor5'),
    '78': ('R6_t-1', 'door_sensor5'),
    '89': ('R6_t',)
}

C = {
    '1': ('Motion_Sensor4', 'R4_t'),
    '2': ('door_sensor4', 'R4_t-1', 'R4_t', 'door_sensor3'),
    '3': ('Camera_sensor2', 'R4_t-1', 'R4_t'),
    '4': ('R5_t-1', 'R4_t-1', 'door_sensor4'),
    '5': ('Motion_Sensor5', 'R5_t'),
    '6': ('door_sensor5', 'R5_t-1', 'R5_t', 'door_sensor4'),
    '7': ('R6_t-1', 'R5_t-1', 'door_sensor5'),
    '8': ('R6_t-1', 'R6_t', 'door_sensor5'),
    '9': ('Motion_Sensor6', 'R6_t')
}


def learn_factor(training_file):
    data = convert_file(training_file)
    bayesian_net = BayesNet(bayesian_network, outcomeSpace=outcomeSpace)
    bayesian_net.learnParameters(data)
    return bayesian_net.factors


def get_room_4_room_5_room_6_model(training_file):
    factor = learn_factor(training_file)
    jt = JoinTree(join_tree, C, S, outcomeSpace)
    jt.distribute_factors(factor.values())
    return jt, bayesian_network
