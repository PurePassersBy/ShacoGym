# Bandit

## Background

Multi-armed bandit is a classic problem to exemplifies the trade-off between **exploration** and **exploitation**.

The name comes from imaging a gambler at a row of slot machines, who has to decide which machines to play, how many times to play each machine and in which order to play them, and whether to continue with the current machine or try a different machine.

## Problem

We takes the most easy variant of this kind of problem. Each machine provides a random reward from a Bernoulli distribution when you pull it. Note the distribution is not known a-priori and you can pull at most $N$ times. The objective of the gambler is to maximize the sum of rewards earned through a sequence of lever pulls. The crucial tradeoff the gambler faces at each trial is between "exploitation" of the machine that has the highest expected payoff and "exploration" to get more information about the expected payoffs of the other machines. 

## Template

```python
class Solution:
    """
        This is the Solution Template for bandit.
        Plz implemnt required functions below, while remain their interface unchanged.
    """
    def setup(self, k: int, quota: int) -> None:
        """
        Called once before the start of the game.
        @param k: number of arms
        @param quota: number of times the agent can pull the arms
        """
        raise NotImplementedError

    def take_action(self) -> int:
        """
        Choose an arm to pull.
        @return: the index of the arm to pull
        """
        raise NotImplementedError

    def on_feedback(self, reward: float) -> None:
        """
        Receive feedback from the environment after taking an action.
        @param reward: the reward received
        """
        raise NotImplementedError
```
