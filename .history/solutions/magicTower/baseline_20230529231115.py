import numpy as np
import math

from typing import List


class MagicUnit:
    def __init__(self, healthpoints: int, attack: int, defence: int, coins: int) -> None:
        self.healthpoints = healthpoints
        self.attack = attack
        self.defence = defence
        self.coins = coins
    
    def attack_mamono(self, mamono: "MagicUnit") -> int:
        give_damage = self.attack - mamono.defence
        receive_damage = mamono.attack - self.defence
        if give_damage <= 0:
            return self.healthpoints
        else:
            defeat_round: int = math.ceil(mamono.healthpoints / give_damage)
            if (final_damage := (defeat_round - 1) * receive_damage) >= self.healthpoints:
                return self.healthpoints
            else:
                return final_damage


class Solution:
    def setup(self, tower_levels: int) -> None:
        """
        Called once before the start of the game.
        @param marker: the tower's total levels.
        """
        self.tower_levels = tower_levels
        self.rng = np.random.default_rng(0)
    
    def take_action(self):
        """
        Choose an action to take.
        @return potion_order: the list of potions order. [healthpoints*100, attack, defence]
        @return raid_order: the list of raid order, which stores road number(0, 1, 2, 3, ect). If num < 0 or num >= level_roads,
                            we will ignore the action. If you donn't walk to the end of one of the road, you will die.
                            Which means the number of choices for one of the roads must to be greater than n.
        """
        potions = self.random_split(self.brave.coins, 3)
        potion_order: List[int] = []
        for i in range(3):
            potion_order.append(len(potions[i]))
        raid_order: List[int] = [0] * self.level_depth
        return potion_order, raid_order
    
    def on_feedback(self, brave: MagicUnit, level_map: List[List[MagicUnit]], level_roads: int, level_depth: int) -> None:
        """
        Receive feedback from the environment after taking an action.
        @param brave: it's your brave!
        @param level_map: the map of current level. It's a two-dimensional array, which full of mamonos.
        @param level_roads: the number of roads.
        @param level_roads: the depth of roads.
        """
        self.brave = brave
        self.level_map = level_map
        self.level_roads = level_roads
        self.level_depth = level_depth

    def random_split(self, n, m=3):
        gids = [np.random.randint(0, m) for i in range(n)]
        buckets = [[k for k in range(n) if gids[k] == i] for i in range(m)]
        return buckets
