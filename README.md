# Markov Process Solver

## Overview

This project involves the creation of a generic Markov process solver that computes optimal policies and values for given states using value iteration and policy improvement algorithms. The solver supports both maximization of rewards and minimization of costs, and can handle decision nodes with specified success rates, as well as chance nodes with given transition probabilities.

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

- **Node/State Names**: Should be alphanumeric.
- **Rewards/Costs**: Lines of the form 'name = value', where value is an integer.
- **Edges**: Of the form 'name : [e1 e2 e3]', where each `e` is the name of an out-edge from `name`.
- **Probabilities**: For chance nodes, 'name % p1 p2 p3'; for decision nodes, 'name % p', with success rates and failure distribution as described.

## Example Usage

```bash
python mdp_solver.py -df 0.9 -max -tol 0.001 -iter 100 example_input.txt
```

## Output

The program outputs the optimal policy (for non-chance nodes) and the values of each state under the optimal policy.

## Implementation Details

he solver implements the algorithm as described, utilizing value iteration to compute state values and greedy policy computation to derive an optimal policy based on the current values. Error handling is included for invalid probability sums and other input inconsistencies.

### Value Iteration

Iteratively updates state values based on the Bellman equation, considering the specified discount factor and the transition probabilities derived from the current policy.

### Greedy Policy Computation

Derives a new policy by selecting actions that maximize rewards (or minimize costs) based on the current state values.

### Handling Different Node Types

The solver differentiates between decision nodes and chance nodes, handling them appropriately according to the input file descriptions.

## Project Structure

The project is structured around modular components for parsing, conversion, and solving, facilitating clear separation of concerns and extendibility. The core modules include:
- `main.py`: The entry point of the program, handling command-line arguments and orchestrating the solving process.
- `markov_solver.py`: Implements the core logic for the Markov process solver, including value iteration and policy computation.
- `policy_computation.py`: Dedicated to computing the optimal policy based on the current value estimates.
- `value_iteration.py`: Contains the implementation of the value iteration algorithm for estimating state values.
- `utils.py`: Provides utility functions for parsing input files and other miscellaneous tasks.
