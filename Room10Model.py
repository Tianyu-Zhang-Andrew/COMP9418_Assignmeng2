from BayesNet import BayesNet
from DataProcessing import convert_file
from Graph import Graph
from JoinTree import JoinTree

outcomeSpace = {
    "Motion_Sensor10": ('motion', 'no motion'),
    "R10_t": ('0', '1', ">1"),
    "R10_t-1": ('0', '1', ">1"),
    "door_sensor11": ('odd', "even", "zero"),
    "door_sensor7": ('odd', "even", "zero")
}

bayesian_network = Graph({
    "Motion_Sensor10": [],
    "R10_t": ["Motion_Sensor10"],
    "R10_t-1": ["R10_t", "door_sensor11", "door_sensor7"],
    "door_sensor11": ["R10_t"],
    "door_sensor7": ["R10_t"]
})

join_tree = Graph({
    '1': ('2',),
    '2': ('1',)
})

S = {
    '12': ('R10_t',)
}

C = {
    '1': ('door_sensor7', 'R10_t', 'R10_t-1', 'door_sensor11'),
    '2': ('R10_t', 'Motion_Sensor10')
}


def learn_factor(training_file):
    data = convert_file(training_file)
    bayesian_net = BayesNet(bayesian_network, outcomeSpace=outcomeSpace)
    bayesian_net.learnParameters(data)
    return bayesian_net.factors


def get_room_10_model(training_file):
    factor = learn_factor(training_file)
    jt = JoinTree(join_tree, C, S, outcomeSpace)
    jt.distribute_factors(factor.values())
    return jt, bayesian_network
