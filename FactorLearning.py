from BayesNet import BayesNet
from DataProcessing import convert_file
from Graph import Graph

G = Graph({
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


def factor_learning(file, graph, outcome_space):
    data = convert_file(file)

    bayesian_network = BayesNet(graph, outcomeSpace=outcome_space)
    bayesian_network.learnParameters(data)

    return bayesian_network.factors
