import time
import math
import itertools
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
    HEALTHPOINTS_UNIT = 100

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
        self.current_level: int = 0
        self.rng = np.random.default_rng(0)
    
    def take_action(self) -> Tuple[List[int], List[int]]:
        """
        Choose an action to take.
        @return potion_order: the list of potions order. [healthpoints*100, attack, defence]
        @return raid_order: the list of raid order, which stores road number(0, 1, 2, 3, ect). If num < 0 or num >= level_roads,
                            we will ignore the action. If you donn't walk to the end of one of the road, you will die.
                            Which means the number of choices for one of the roads must to be greater than n.
        """
        self.potion_order: List[int] = self.random_split(self.brave.coins, 3)
        self.raid_order: List[int] = [0] * self.level_depth
        self.best_value: float = 0.
        self.search_road(0, [0] * self.level_roads)
        return self.potion_order, self.raid_order

    def evaluate_action(self, potion_order: List[int], raid_order: List[int]) -> float:
        brave = MagicUnit(
            self.brave.healthpoints + potion_order[0] * self.HEALTHPOINTS_UNIT,
            self.brave.attack + potion_order[1],
            self.brave.defence + potion_order[2],
            0
        )
        current_depths: List[int] = [0] * self.level_roads
        n_steps: int = 0
        for road in raid_order:
            depth = current_depths[road]
            damage = brave.test_attack_mamono(self.level_map[road][depth])
            if damage >= brave.healthpoints:
                return 0.
            brave.healthpoints -= damage
            current_depths[road] += 1
            n_steps += 1
            if current_depths[road] == self.level_depth:
                break
        value = brave.healthpoints / self.HEALTHPOINTS_UNIT + brave.attack + brave.defence  # TODO: consider coins, score, speed
        return value

    def search_potion(self, depths: List[int]):
        for hp in range(self.brave.coins+1):
            for at in range(self.brave.coins+1-hp):
                df = self.brave.coins - hp - at
                potion_order = [hp, at, df]
                raid_order = list(itertools.chain.from_iterable([road] * depth for road, depth in enumerate(depths)))
                for _ in range(10):
                    np.random.shuffle(raid_order)
                    value = self.evaluate_action(potion_order, raid_order)
                    if self.best_value < value:
                        self.best_value = value
                        self.potion_order, self.raid_order = potion_order, raid_order

    def search_road(self, i_road: int, depths: List[int]):
        if i_road == self.level_roads:
            n_ends = sum(depth == self.level_depth for depth in depths)
            if n_ends != 0:
                self.search_potion(depths)
            return
        # print(i_road, depths)
        for depth in range(0, self.level_depth + 1):
            depths[i_road] = depth
            if depth == self.level_depth:
                self.search_road(self.level_roads, depths)
            else:
                self.search_road(i_road + 1, depths)
            depths[i_road] = 0
    
    def on_feedback(self, brave: MagicUnit, level_map: List[List[MagicUnit]]) -> None:
        """
        Receive feedback from the environment after taking an action.
        @param brave: it's your brave!
        @param level_map: the map of current level. It's a two-dimensional array, which full of mamonos.
        """
        self.brave = brave
        self.level_map = level_map
        self.level_roads, self.level_depth = len(level_map), len(level_map[0])
        self.current_level += 1

    def random_split(self, n: int, m: int) -> List[int]:
        rng = np.random.RandomState(int(time.time()))
        buckets = [0] * m
        for _ in range(n):
            buckets[rng.randint(0, m)] += 1
        return buckets
