# Markov Process Solver

## Overview

This Markov Decision Process (MDP) solver is designed to determine optimal policies and value functions for decision-making problems modeled as MDPs. Utilizing both value iteration and policy improvement techniques, it handles decision and chance nodes, accommodating both reward maximization and cost minimization strategies. The solver's has support for configurable discount factors, tolerance levels, and iteration limits, ensuring robust and precise solutions across various scenarios.

## Features

- **Discount Factor**: Supports specifying a discount factor for future rewards or costs.
- **Maximize Rewards or Minimize Costs**: Can be configured to either maximize rewards or minimize costs based on the flags provided.
- **Tolerance for Value Iteration**: Allows setting a tolerance level for the convergence of value iteration.
- **Iteration Cutoff**: Supports specifying a maximum number of iterations for value iteration.

## Requirements

- Python 3.8 or higher

## Installation

No specific installation steps are required other than having a Python interpreter. Clone the repository or download the source code to get started.

## Usage

To run the program, use the following command format:

```bash
python mdp_solver.py -df <discount_factor> [-max] [-tol <tolerance>] [-iter <iterations>] <input_file.txt>
```

- `-df <discount_factor>`: Sets the discount factor for future rewards/costs.
- `-max`: Specifies that the solver should maximize rewards (default is to minimize costs).
- `-tol <tolerance>`: Sets the tolerance level for exiting value iteration.
- `-iter <iterations>`: Specifies a cutoff for the number of iterations in value iteration.
- `<input_file.txt>`: The path to the input file containing the Markov decision process description.

## Input File Format

The input file should be structured as follows:

- **Node/State Names**: Should be alphanumeric.
- **Rewards/Costs**: Lines of the form 'name = value', where value is an integer.
- **Edges**: Of the form 'name : [e1 e2 e3]', where each `e` is the name of an out-edge from `name`.
- **Probabilities**: For chance nodes, 'name % p1 p2 p3'; for decision nodes, 'name % p', with success rates and failure distribution as described.

Example:
```
A = 10
B : [A, B]
B % 0.8 0.2
```

## Example Usage

```bash
python mdp_solver.py -df 0.9 -max -tol 0.001 -iter 100 example_input.txt
```

## Output

The program outputs the optimal policy (for non-chance nodes) and the values of each state under the optimal policy.

## Implementation Details

The solver implements the algorithm as described, utilizing value iteration to compute state values and greedy policy computation to derive an optimal policy based on the current values. Error handling is included for invalid probability sums and other input inconsistencies.

### Value Iteration

Iteratively updates state values based on the Bellman equation, considering the specified discount factor and the transition probabilities derived from the current policy.

### Greedy Policy Computation

Derives a new policy by selecting actions that maximize rewards (or minimize costs) based on the current state values.

### Handling Different Node Types

The solver differentiates between decision nodes and chance nodes, handling them appropriately according to the input file descriptions.

## Project Structure

The project is structured around modular components for parsing, and solving, facilitating clear separation of concerns and extendibility. The core components include:

- **`Node` Class**: Central to defining the states within the Markov Decision Process, it encapsulates each state's rewards, transitions, and probabilities. Critical for establishing the structure upon which policies and values are calculated.

- **`Graph` Class**: Responsible for constructing the MDP's graph representation. It aggregates `Node` instances, forming the MDP's complete state-action graph. This component is key for organizing the MDP's structure and facilitating the subsequent solving process.

- **`MDPSolver` Class**: The driving force behind solving the MDP, employing value iteration and policy improvement algorithms to determine optimal state values and policies. It iteratively refines policies and values, leveraging the graph structure to achieve convergence to optimal solutions.

- **Input Parsing**: Integrated within the `Graph` class, this functionality interprets and transforms input data into a structured graph format. It ensures the accurate representation of the MDP's states, actions, and transitions as defined by the input specifications.

- **Value Iteration and Policy Improvement**: Embedded within the `MDPSolver` class, these algorithms form the core computational mechanisms of the solver. Value iteration updates state values based on the Bellman equation, while policy improvement iteratively refines the policy towards optimality.