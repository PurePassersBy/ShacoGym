import argparse

from gym import Gym


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--problem_name', '-p', type=str)
    parser.add_argument('--solution_file', '-s', type=str)
    parser.add_argument('--mode', '-m', type=str, default='solve', choices=['solve', 'play'])
    args = parser.parse_args()

    gym = Gym()

    if args.mode == 'solve':
        gym.solve(args.problem_name, args.solution_file)
    elif args.mode == 'play':
        gym.play(args.problem_name)
    else:
        raise ValueError(f"Unknown mode: {args.mode}")
