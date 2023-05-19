# Bandit

## Background

Multi-armed bandit is a classic problem to exemplifies the trade-off between **exploration** and **exploitation**.

The name comes from imaging a gambler at a row of slot machines, who has to decide which machines to play, how many times to play each machine and in which order to play them, and whether to continue with the current machine or try a different machine.

## Problem

We takes the most easy variant of this kind of problem. Each machine provides a random reward from a Bernoulli distribution when you pull it. Note the distribution is not known a-priori and you can pull at most $N$ times. The objective of the gambler is to maximize the sum of rewards earned through a sequence of lever pulls. The crucial tradeoff the gambler faces at each trial is between "exploitation" of the machine that has the highest expected payoff and "exploration" to get more information about the expected payoffs of the other machines. 
