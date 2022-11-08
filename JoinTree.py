from DiscreteFactors import Factor
from EliminationTree import EliminationTree
import graphviz


class JoinTree(EliminationTree):
    def __init__(self, graph, clusters, separators, outcomeSpace):
        self.graph = graph
        self.separators = separators # dict mapping each edge node1+node2 -> tuple of separator vars
        self.clusters = clusters
        self.outcomeSpace = outcomeSpace

        self.factors = {}
        for node in self.graph:
            # trivial factor (Factor's initialize to all 1's by default)
            self.factors[node] = Factor(self.clusters[node], outcomeSpace)

        self.messages = None

    def show(self, positions=None):
        '''
        A specialised function to show JoinTrees, including the separators and clusters
        '''
        dot = graphviz.Graph(engine="neato", comment='Undirected graph', strict=True)
        dot.attr(overlap="false", splines="true")
        for v in self.graph:
            if positions is not None:
                dot.node(str(v), label=str(v)+'\n'+','.join(self.clusters[v]), pos=positions[v])
            else:
                dot.node(str(v), label=str(v)+'\n'+','.join(self.clusters[v]))
        for v in self.graph:
            for w in self.graph.children(v):
                if v < w:
                    dot.edge(str(v), str(w), ','.join(self.separators[str(v)+str(w)]))

        return dot

    def distribute_factors(self, factor_list):
        '''
        Takes a list of factors and adds them one by one to the jointree
        '''
        for factor in factor_list:
            for node in self.graph:
                # We will find a match if the factor domain is a subset of the cluster (trivial factor) domain
                if set(factor.domain).issubset(self.clusters[node]):
                    self.factors[node] *= factor
                    break
            else:
                # This else clause will only be executed if the for loop reaches the end. Google "python for/else" for more info
                raise NameError('FamilyPreservationError')