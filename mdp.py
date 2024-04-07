import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Markov Decision Process Solver')
    
    parser.add_argument('-df', nargs='?', type=float, required=False, default=1.0, help='Discount factor [0, 1] for future rewards. Default is 1.0.')
    parser.add_argument('-max', required=False, action='store_true', help='Maximize rewards. Default to false which minimizes costs.')
    parser.add_argument('-tol', nargs='?', default=0.01, type=float, required=False, help='Tolerance for exiting value iteration. Default is 0.01.')
    parser.add_argument('-iter', nargs='?', default=100, type=float, required=False, help='Cutoff for value iteration. Default is 100.')
    parser.add_argument('input_file', type=str, help='Path to the input file.')

    args = parser.parse_args()

    return args

def main():
    args = parse_arguments()
    print(f"Arguments: {args}")

    print(f"Discount Factor: {args.df}")
    print(f"Maximize Rewards: {args.max}")
    print(f"Tolerance: {args.tol}")
    print(f"Iterations: {args.iter}")
    print(f"Input File: {args.input_file}")

if __name__ == "__main__":
    main()
