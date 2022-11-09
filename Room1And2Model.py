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


def learn_factor(training_file):
    data = convert_file(training_file)
    bayesian_net = BayesNet(bayesian_network, outcomeSpace=outcomeSpace)
    bayesian_net.learnParameters(data)
    return bayesian_net.factors


def get_room_1_room_2_model(training_file):
    factor = learn_factor(training_file)
    jt = JoinTree(join_tree, C, S, outcomeSpace)
    jt.distribute_factors(factor.values())
    return jt, bayesian_network
