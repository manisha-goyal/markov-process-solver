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
        self.type = ""

    def set_reward(self, reward):
        self.reward = reward
        self.value = reward
    
    def set_edges(self, edges):
        self.edges = edges

    def set_probabilities(self, probabilities):
        self.probabilities = probabilities

    def set_success_rate(self, success_rate):
        self.success_rate = success_rate

    def set_node_type(self):
        if self.is_decision_node:
            self.type = "Decision Node" 
        elif self.is_terminal():
            self.type = "Terminal Node"
        else:
            self.type = "Chance Node"
    
    def process_probabilities(self):
        if self.is_terminal() and len(self.probabilities) >= 1:
            print(f"Error: {self.name} is a terminal node but probability entry is given.")
            sys.exit()

        if len(self.edges) == 1:
            print_debug(f"Setting chance node: {self.name}")
            self.edges_probs[self.edges[0]] = self.probabilities[0] if len(self.probabilities) == 1 else 1.0
        elif len(self.edges) > 1:
            if len(self.probabilities) > 1:
                print_debug(f"Setting chance node: {self.name}")
                if sum(self.probabilities) != 1.0:
                    print("The probabilities must add up to 1")
                    sys.exit(1)
                if len(self.edges) != len(self.probabilities):
                    print(f"Error: Number of edges does not match number of probabilities for {self.name}.")
                    sys.exit()

                for edge, probability in zip(self.edges, self.probabilities):
                    self.edges_probs[edge] = probability
            else:
                print_debug(f"Setting decision node: {self.name}")
                success_rate = self.probabilities[0] if len(self.probabilities) == 1 else 1.0
                failure_rate = (1 - success_rate) / (len(self.edges) - 1) if len(self.probabilities) == 1 else 0
                self.set_success_rate(success_rate)
                self.is_decision_node = True
                for edge in self.edges:
                    self.edges_probs[edge] = success_rate if edge == self.edges[0] else failure_rate
    
    def is_terminal(self):
        return not self.edges
    
    def __repr__(self):
        return (f"Node({self.name}, Reward={self.reward}, Value={self.value}, Edge Probabilities={[(edge, '%.3f' % round(prob, 4)) for edge, prob in self.edges_probs.items()]}, Type={self.type})")

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)
        return self.nodes[name]
    
    def get_values(self):
        return {name: node.value for name, node in self.nodes.items()}

    def create_graph(self, file_path):
        print_debug(f"\n\nParsing input")
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
            node.set_node_type()

        print_debug(f"\nParsed Graph: \n{repr(self)}")

    def __repr__(self):
        newline = "\n"
        nodes_repr = f",{newline}".join([repr(node) for node in self.nodes.values()])
        return f"Graph[{newline}{nodes_repr}{newline}]"
    
class MDPSolver:
    def __init__(self, graph, df=1.0, tol=0.01, iter=100, is_max=True):
        self.graph = graph
        self.df = df
        self.tol = tol
        self.iter = iter
        self.is_max = is_max
        self.policies = {}

    def get_policies(self):
        return {state: action for state, action in self.policies.items()}
    
    def set_initial_policy(self):
        for state, node in graph.nodes.items():
            if node.is_decision_node:
                self.policies[state] = node.edges[0]

    def solve(self):
        print_debug("\n\nMDP Solver")
        self.set_initial_policy()
        print_debug(f"Initial policies: {self.policies}")
        while True:
            curr_policy = self.policies
            self.value_iteration()
            self.greedy_policy_computation()
            new_policy = self.policies
            self.apply_policy()
            if curr_policy == new_policy:
                break
        print_debug(f"\nFinal values: {self.graph.get_values()}")
        print_debug(f"Optimal policies: {self.get_policies()}")
        
        self.print_solution()

    def apply_policy(self):
        for name, node in self.graph.nodes.items():
            if node.is_decision_node:
                action = self.policies.get(name, None)
                if action:
                    for edge in node.edges:
                        node.edges_probs[edge] = node.success_rate if edge == action else (1 - node.success_rate) / (len(node.edges) - 1)

    def value_iteration(self):
        print_debug(f"Value iteration:")
        old_values = self.graph.get_values()
        for i in range(self.iter):
            max_diff = 0
            for _, node in self.graph.nodes.items():
                if node.is_terminal():
                    continue
                old_value = node.value
                expected_utility = 0
                for edge, probability in node.edges_probs.items():
                    expected_utility += probability * self.graph.nodes[edge].value
                
                node.value = node.reward + (self.df * expected_utility)
                max_diff = max(max_diff, abs(old_value - node.value))
            print_debug(f"Value Iteration: {i}")
            print_debug(f"Previous values: {old_values}")
            print_debug(f"Current values: {self.graph.get_values()}")
            if max_diff < self.tol:
                print_debug(f"The values are equal")
                break
        print_debug(f"Values: {self.graph.get_values()}")

    def greedy_policy_computation(self):
        print_debug(f"Greedy policy computation:")
        updated = False
        new_policy = {} 
        
        for name, node in self.graph.nodes.items():
            if node.is_decision_node:
                print_debug(f"Computing policy for node: {name}")
                utilities = {}
                
                for action in node.edges:
                    probabilities = {edge: node.success_rate if edge == action else (1 - node.success_rate) / (len(node.edges) - 1) for edge in node.edges}
                    exp_edge_value = 0
                    for edge, prob in probabilities.items():
                        exp_edge_value += prob * self.graph.nodes[edge].value
                    utilities[action] = node.reward + (self.df * exp_edge_value)
                    print_debug(f"\tPolicy: {name} -> {action} has a value of {utilities[action]}")
                
                best_action = max(utilities, key=utilities.get) if self.is_max else min(utilities, key=utilities.get)
                print_debug(f"\tBest policy: {name}: {node.name} -> {best_action}")

                current_action = self.policies.get(name, None)
                if best_action != current_action:
                    new_policy[name] = best_action
                    updated = True
                else:
                    new_policy[name] = current_action
        
        print_debug(f"Previous policies: {self.get_policies()}")
        if updated:
            self.policies = new_policy
        print_debug(f"Current policies: {self.get_policies()}")

    def print_solution(self):
        print_debug("\n\nFinal solution: \n")
        policies = []
        for src, dest in self.get_policies().items():
            if len(self.graph.nodes[src].edges) > 1:
                policies.append(f"{src} -> {dest}")

        for line in sorted(policies):
            print(line)

        values = []
        for node_name, node in self.graph.nodes.items():
            values.append(f"{node_name}={node.value:.3f}")
        
        print("\n" + " ".join(sorted(values)))
        
def print_debug(*args, **kwargs):
    if debug:
        print(*args, **kwargs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Markov Decision Process Solver')
    parser.add_argument('-df', nargs='?', type=float, required=False, default=1.0, help='Discount factor [0, 1] for future rewards. Default is 1.0.')
    parser.add_argument('-max', required=False, action='store_true', help='Maximize rewards. Default to false which minimizes costs.')
    parser.add_argument('-tol', nargs='?', default=0.01, type=float, required=False, help='Tolerance for exiting value iteration. Default is 0.01.')
    parser.add_argument('-iter', nargs='?', default=100, type=int, required=False, help='Cutoff for value iteration. Default is 100.')
    parser.add_argument('input_file', type=str, help='Path to the input file.')
    parser.add_argument('-debug', required=False, action='store_true', help='Flag for debug printing')
    args = parser.parse_args()

    debug = args.debug

    graph = Graph()
    graph.create_graph(args.input_file)
    solver = MDPSolver(graph, args.df, args.tol, args.iter, args.max)
    solver.solve()
