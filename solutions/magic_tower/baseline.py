import time
import math
from typing import List, Tuple

import numpy as np


class MagicUnit:
    def __init__(self, healthpoints: int, attack: int, defence: int, coins: int) -> None:
        self.healthpoints = healthpoints
        self.attack = attack
        self.defence = defence
        self.coins = coins
    
    def test_attack_mamono(self, mamono: "MagicUnit") -> int:
        give_damage = self.attack - mamono.defence
        receive_damage = mamono.attack - self.defence if (mamono.attack - self.defence > 0) else 0
        if give_damage <= 0:
            return self.healthpoints
        else:
            defeat_round: int = math.ceil(mamono.healthpoints / give_damage)
            if (final_damage := (defeat_round - 1) * receive_damage) >= self.healthpoints:
                return self.healthpoints
            else:
                return final_damage


class Solution:
    def setup(self, tower_levels: int, brave: MagicUnit, level_map: List[List[MagicUnit]]) -> None:
        """
        Called once before the start of the game.
        @param tower_levels: the number of levels in the tower.
        @param brave: the brave with four attributes: healthpoints, attack, defence, coins.
        @param level_map: a 2D map of the first floor.
        """
        self.tower_levels = tower_levels
        self.brave = brave
        self.level_map = level_map
        self.level_roads, self.level_depth = len(level_map), len(level_map[0])
        self.rng = np.random.default_rng(0)
    
    def take_action(self) -> Tuple[List[int], List[int]]:
        """
        Choose an action to take.
        @return potion_order: the list of potions order. [healthpoints*100, attack, defence]
        @return raid_order: the list of raid order, which stores road number(0, 1, 2, 3, ect). If num < 0 or num >= level_roads,
                            we will ignore the action. If you donn't walk to the end of one of the road, you will die.
                            Which means the number of choices for one of the roads must to be greater than n.
        """
        potion_order: List[int] = self.random_split(self.brave.coins, 3)
        raid_order: List[int] = [0] * self.level_depth
        return potion_order, raid_order
    
    def on_feedback(self, brave: MagicUnit, level_map: List[List[MagicUnit]]) -> None:
        """
        Receive feedback from the environment after taking an action.
        @param brave: it's your brave!
        @param level_map: the map of current level. It's a two-dimensional array, which full of mamonos.
        """
        self.brave = brave
        self.level_map = level_map
        self.level_roads, self.level_depth = len(level_map), len(level_map[0])

    def random_split(self, n: int, m: int) -> List[int]:
        rng = np.random.RandomState(int(time.time()))
        buckets = [0] * m
        for _ in range(n):
            buckets[rng.randint(0, m)] += 1
        return buckets
