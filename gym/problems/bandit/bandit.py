import time
from typing import List

import numpy as np

from ..base import Environment


class InteractivePlayer:
    def setup(self, k: int, quota: int) -> None:
        self.k = k
        self.quota = quota
        print('=== Welcome to ShacoGym. This is a Bandit game. ===')
        print('In this game, you are facing a slot machine with 2 arms.\n\n'
              'Each arm has a different probability of giving you a reward.'
              'Each round you can pull only one arm\n\n'
              'Your goal is to maximize the total reward you get in 10 rounds.\n')

    def take_action(self) -> int:
        while True:
            action = input('Enter your action: ')
            if action.isdigit():
                action = int(action)
                if action in range(self.k):
                    return action
            print('Invalid action. Please try again.')

    def on_feedback(self, reward: float) -> None:
        print(f'You get reward: {reward}')


class Bandit(Environment):
    RESULTS: List[int] = []

    def __init__(self, k: int, probs: List[float], quota: int, seed: int=0):
        self.k = k
        self.probs = probs
        self.quota = quota
        self.seed = seed

    def setup(self):
        self.rng = np.random.default_rng(self.seed)  # for reproducibility
        self.total_reward = 0.
        return {"k": self.k, "quota": self.quota}

    def set_logger(self, logger):
        self.logger = logger

    def run(self, sol):
        for idx in range(self.quota):
            action = sol.take_action()
            reward = self.on_action(action)
            sol.on_feedback(reward)

            self.total_reward += reward
            # self.logger.info(f'{idx+1} / {self.quota}: Agent takes action: {action}, gets reward: {reward}')

        self.logger.info(f"Total reward: {self.total_reward}")
        self.RESULTS.append(int(self.total_reward))

    def on_action(self, index: int) -> float:
        if self.rng.random() < self.probs[index]:
            return 1.
        return 0.

    @classmethod
    def show_results(cls):  # TODO: Better visualization
        print("\nYour results:")
        print("|         |  1  |  2  |  3  |  4  |")
        print(" --------- ----- ----- ----- ------")
        print(" Baseline |  58 | 517 |  28 | 267 |")
        print(" --------- ----- ----- ----- ------")
        print(" SOTA     |  84 | 972 |  32 | 426 |")
        print(" --------- ----- ----- ----- ------")
        print(f" Yours    | {cls.RESULTS[0]:3d} | {cls.RESULTS[1]:3d} | {cls.RESULTS[2]:3d} | {cls.RESULTS[3]:3d} |")

    @classmethod
    def from_file(cls, file_path: str):
        pass

    @classmethod
    def show_baseline_results(cls):
        print("\nBaseline results:")
        print("|  1  |  2  |  3  |  4  |")
        print(" ----- ----- ----- ------")
        print("|  58 | 517 | 28  | 267 |")

    @classmethod
    def show_sota_results(cls):
        print("\nSOTA results:")
        print("|  1  |  2  |  3  |  4  |")
        print(" ----- ----- ----- ------")
        print("| 84  | 972 | 32  | 426 |")

    @classmethod
    def from_play_mode(cls):
        seed = int(time.time())
        return cls(2, [0.4, 0.65], 10, seed)
    
    @classmethod
    def get_interactive_player(cls):
        return InteractivePlayer
