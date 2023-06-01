import time
import math
from copy import deepcopy
from typing import Any, List

import numpy as np

from ..base import Environment


POTION_CATEGORY: int = 3
HEALTHPOINTS_UNIT: int = 100


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
            
    def attack_mamono(self, mamono: "MagicUnit") -> None:
        give_damage = self.attack - mamono.defence
        receive_damage = mamono.attack - self.defence if (mamono.attack - self.defence > 0) else 0
        final_damage: int = 0
        if give_damage <= 0:
            final_damage = self.healthpoints
        else:
            defeat_round: int = math.ceil(mamono.healthpoints / give_damage)
            if (final_damage := (defeat_round - 1) * receive_damage) >= self.healthpoints:
                final_damage = self.healthpoints
            else:
                final_damage = final_damage
        self.healthpoints -= final_damage
        self.coins += mamono.coins
        
    def drink_potion(self, potion: "MagicUnit") -> None:
        if potion.coins == 0:
            self.healthpoints += potion.healthpoints
            self.attack += potion.attack
            self.defence += potion.defence


class InteractivePlayer:  # TODO: InteractivePlayer
    ...


class MagicTower(Environment):
    SCORES: List[float] = []

    def __init__(
        self,
        seed: int,
        healthpoints: int,
        attack: int,
        defence: int,
        coins: int,
        difficulty: int,
        tower_levels: int,
        level_roads: int,
        level_depth: int
    ) -> None:
        self.seed = seed
        self.brave = MagicUnit(healthpoints, attack, defence, coins)
        self.tower_levels = tower_levels
        self.difficulty = difficulty
        self.level_roads = level_roads
        self.level_depth = level_depth

    def setup(self):
        self.rng = np.random.RandomState(self.seed)
        self.score: float = 0.
        self.level_map = self.build_level(level=0)
        return {'tower_levels': self.tower_levels, 'brave': deepcopy(self.brave), 'level_map': deepcopy(self.level_map)}
    
    def run(self, sol):
        for level in range(self.tower_levels):
            potion_order, raid_order = sol.take_action()  # TODO: fine-grained action
            action_result = self.on_action(potion_order, raid_order, level)
            if action_result is False:
                self.logger.info(f'Dead! Final score: {self.score:.4f}')
                break
            if level == self.tower_levels - 1:
                self.logger.info(f'Congratulations! You have passed through the tower! Final score: {self.score:.4f}!')
                break
            self.logger.info(f'Next level! Current score: {self.score:.4f}')
            self.level_map = self.build_level(level + 1)
            sol.on_feedback(deepcopy(self.brave), deepcopy(self.level_map))
        self.SCORES.append(self.score)

    def on_action(self, potion_order: List[int], raid_order: List[int], level: int):
        self.drink_potion(potion_order)
        return self.raid_by_order(level, raid_order, self.level_map)
    
    def build_level(self, level: int) -> List[List[MagicUnit]]:
        self.level_score: int = 0
        level_map: List[List[MagicUnit]] = [[MagicUnit(0, 0, 0, 0)] * self.level_depth for _ in range(self.level_roads)]
        for i in range(self.level_roads):
            for j in range(self.level_depth):
                coins: int = int(self.difficulty * self.rng.uniform(1, 2))  # TODO: general way to generate coins
                unit_difficulty = coins * (level + 1)
                healthpoints, attack, denfence = self.random_split(unit_difficulty-3, 3)
                healthpoints = (healthpoints + 1) * HEALTHPOINTS_UNIT
                attack = attack + 1
                denfence = denfence + 1
                level_map[i][j] = MagicUnit(healthpoints, attack, denfence, int(coins/4))
                self.level_score += unit_difficulty
        return level_map
    
    def drink_potion(self, potion_order: List[int]):
        potions_cost: int = sum(potion_order)
        if potions_cost > self.brave.coins:
            raise AssertionError("The cost of potions exceeds your coins!")
        for potion in potion_order:
            if potion < 0:
                raise AssertionError("The quantity of potion is smaller than zero!")
        self.brave.coins -= potions_cost
        self.brave.drink_potion(MagicUnit(potion_order[0]*HEALTHPOINTS_UNIT, potion_order[1], potion_order[2], 0))

    def raid_by_order(self, level: int, raid_order: List[int], level_map: List[List[MagicUnit]]) -> bool:
        roads_depth_now: List[int] = [0] * self.level_roads
        for i, order in enumerate(raid_order):
            if order < 0 or order >= self.level_roads:
                raise AssertionError("The number of the road is incorrect.")
            attacked_mamono = level_map[order][roads_depth_now[order]]
            self.brave.attack_mamono(attacked_mamono)
            if self.brave.healthpoints == 0:
                return False
            self.score += attacked_mamono.coins * (level + 1)
            roads_depth_now[order] += 1
            if roads_depth_now[order] == self.level_depth:
                self.score += self.level_score * (1 - (i / (self.level_roads * self.level_depth)))
                return True
        return False
    
    @classmethod
    def show_results(cls):
        print('\nYour results:')
        print(f'Total scores: {sum(cls.SCORES):.4f}')

    @classmethod
    def from_play_mode(cls) -> "MagicTower":
        raise NotImplementedError

    @classmethod
    def get_interactive_player(cls):
        return InteractivePlayer

    def random_split(self, n: int, m: int) -> List[int]:
        buckets = [0] * m
        for _ in range(n):
            buckets[self.rng.randint(0, m)] += 1
        return buckets
