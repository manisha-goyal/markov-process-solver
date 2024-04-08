import argparse, sys

debug = False

class Node:
    def __init__(self, name):
        self.name = name
        self.reward = 0
        self.value = 0
        self.edges = [] 
        self.probabilities = []
        self.success_rate = None
        self.is_decision_node = False
        self.edges_probs = {}

    def set_reward(self, reward):
        self.reward = reward
        self.value = reward
    
    def set_edges(self, edges):
        self.edges = edges

    def set_probabilities(self, probabilities):
        self.probabilities = probabilities

    def set_success_rate(self, success_rate):
        self.success_rate = success_rate

    def set_node_type(self, type):
        if type == 'decision':
            self.is_decision_node = True;
    
    def process_probabilities(self):
        if self.is_terminal() and len(self.probabilities) >= 1:
            print(f"Error: {self.name} is a terminal node but probability entry is given.")
            sys.exit()

        if len(self.probabilities) <= 1:
            success_rate = self.probabilities[0] if len(self.probabilities) == 1 else 1.0
            failure_rate = (1 - success_rate) / max(len(self.edges) - 1, 1) if len(self.probabilities) == 1 else 0
            self.set_success_rate(success_rate)
            self.set_node_type('decision')
            for edge in self.edges:
                self.edges_probs[edge] = success_rate if edge == self.edges[0] else failure_rate
        else:
            if sum(self.probabilities) != 1.0:
                    print("The probabilities must add up to 1")
                    sys.exit(1)
            if len(self.edges) != len(self.probabilities):
                print(f"Error: Number of edges does not match number of probabilities for {self.name}.")
                sys.exit()

            for edge, probability in zip(self.edges, self.probabilities):
                self.edges_probs[edge] = probability
    
    def is_terminal(self):
        return not self.edges
    
    def __repr__(self):
        return (f"Node({self.name}, Reward={self.reward}, Edges Probs={[(a, '%.3f' % round(b, 4)) for a, b in self.edges_probs.items()]}, "
                f"Terminal Node={self.is_terminal()}, Decision Node={self.is_decision_node}, Chance Node={not self.is_decision_node})")

class Graph:
    def __init__(self, df, tol, iter, is_max):
        self.nodes = {}
        self.df = df
        self.tol = tol
        self.iter = iter
        self.is_max = is_max
        self.nodes = {}

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)
        return self.nodes[name]

    def create_graph(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#') or not line:
                    print_debug(f"{'Empty line' if len(line) == 0 else 'Comment'} - {line}")
                    continue

                if '=' in line:
                    print_debug(f"Reward - {line}")
                    name, value = line.split('=')
                    node = self.add_node(name.strip())
                    node.set_reward(float(value.strip()))

                elif ':' in line:
                    print_debug(f"Edges - {line}")
                    name, edges_str = line.split(':')
                    edges = [edge.strip() for edge in edges_str.strip()[1:-1].split(',')]
                    node = self.add_node(name.strip())
                    node.set_edges(edges)
                    for edge in edges:
                        self.add_node(edge)

                elif '%' in line:
                    print_debug(f"Probabilities - {line}")
                    name, probs_str = line.split('%')
                    probabilities = [float(p.strip()) for p in probs_str.strip().split()]
                    node = self.add_node(name.strip())
                    node.set_probabilities(probabilities)
                
                else:
                    print_debug(f"Invalid line - {line}")
                    print(f"Input line does not follow expected format: {line}")
                    sys.exit()
        
        for name, node in self.nodes.items():
            node.process_probabilities()

    def __repr__(self):
        node_summaries = ', '.join([node.name for node in self.nodes.values()])
        return (f"Graph(Discount Factor={self.df}, Tolerance={self.tol}, Iterations={self.iter}, "
                f"Maximize Rewards={self.is_max}, Nodes=[{node_summaries}])")

def print_debug(*args, **kwargs):
    if debug:
        print(*args, **kwargs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Markov Decision Process Solver')
    parser.add_argument('-df', nargs='?', type=float, required=False, default=1.0, help='Discount factor [0, 1] for future rewards. Default is 1.0.')
    parser.add_argument('-max', required=False, action='store_true', help='Maximize rewards. Default to false which minimizes costs.')
    parser.add_argument('-tol', nargs='?', default=0.01, type=float, required=False, help='Tolerance for exiting value iteration. Default is 0.01.')
    parser.add_argument('-iter', nargs='?', default=100, type=float, required=False, help='Cutoff for value iteration. Default is 100.')
    parser.add_argument('input_file', type=str, help='Path to the input file.')
    parser.add_argument('-debug', required=False, action='store_true', help='Flag for debug printing')
    args = parser.parse_args()

    debug = args.debug

    graph = Graph(args.df, args.tol, args.iter, args.max)
    graph.create_graph(args.input_file)

    if debug:
        print("\nParsed Graph:")
        print(graph)

        print("\nParsed Nodes:")
        for node in graph.nodes.values():
            print(node)
