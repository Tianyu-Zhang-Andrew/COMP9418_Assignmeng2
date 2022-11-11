from BayesNet import BayesNet
from DataProcessing import convert_file
from Graph import Graph
from JoinTree import JoinTree

outcomeSpace = {
    "Motion_Sensor9": ('motion', 'no motion'),
    "R9_t": ('0', '1', ">1"),
    "R9_t-1": ('0', '1', ">1"),
    "door_sensor6": ('odd', "even", "zero")
}

bayesian_network = Graph({
    "Motion_Sensor9": [],
    "R9_t": ["Motion_Sensor9"],
    "R9_t-1": ["R9_t", "door_sensor6"],
    "door_sensor6": ["R9_t"]
})

join_tree = Graph({
    '1': ('2',),
    '2': ('1',)
})

S = {
    '12': ('R9_t',)
}

C = {
    '1': ('door_sensor6', 'R9_t', 'R9_t-1'),
    '2': ('R9_t', 'Motion_Sensor9')
}


def learn_factor(training_file):
    data = convert_file(training_file)
    bayesian_net = BayesNet(bayesian_network, outcomeSpace=outcomeSpace)
    bayesian_net.learnParameters(data)
    return bayesian_net.factors


def get_room_9_model(training_file):
    factor = learn_factor(training_file)
    jt = JoinTree(join_tree, C, S, outcomeSpace)
    jt.distribute_factors(factor.values())
    return jt, bayesian_network
