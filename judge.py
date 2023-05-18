import argparse

from gym import Gym


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--problem_name', '-p', type=str)
    parser.add_argument('--solution_file', '-s', type=str)
    args = parser.parse_args()

    gym = Gym()
    gym.run(args.problem_name, args.solution_file)