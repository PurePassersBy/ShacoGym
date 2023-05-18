import random


class Solution:
    def setup(self, k: int, quota: int) -> None:
        """
        Called once before the start of the game.
        @param k: number of arms
        @param quota: number of times the agent can pull the arms
        """
        self.k = k
        random.seed(0)

    def take_action(self) -> int:
        return random.randint(0, self.k - 1)

    def on_feedback(self, reward: float) -> None:
        pass