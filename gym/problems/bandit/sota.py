from scipy.stats import beta


class Solution:
    def setup(self, k: int, quota: int) -> None:
        """
        Called once before the start of the game.
        @param k: number of arms
        @param quota: number of times the agent can pull the arms
        """
        self.k = k

        self.c = 3
        self._as = [1.] * k
        self._bs = [1.] * k

        self.i = 0

    def take_action(self) -> int:
        self.i = max(
            range(self.k),
            key=lambda x: self._as[x] / (self._as[x] + self._bs[x]) + float(beta.std(self._as[x], self._bs[x]) * self.c)
        )
        return self.i

    def on_feedback(self, reward: float) -> None:
        self._as[self.i] += reward
        self._bs[self.i] += 1 - reward
