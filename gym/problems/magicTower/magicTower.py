import time
import math
from copy import deepcopy
from typing import Any, List
import numpy as np
from ..base import Environment

POTION_CATEGORY: int = 3


class MagicUnit:
    def __init__(self, healthpoints: int, attack: int, defence: int, coins: int) -> None:
        self.healthpoints = healthpoints
        self.attack = attack
        self.defence = defence
        self.coins = coins
    
    def attack_mamono(self, mamono: "MagicUnit") -> int:
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
    
    def drink_potion(self, potion: "MagicUnit") -> int:
        if potion.coins == 0:
            self.healthpoints += potion.healthpoints
            self.attack += potion.attack
            self.defence += potion.defence

class InteractivePlayer: # TODO: InteractivePlayer
    ...

class MagicTower(Environment):
    SCORES: List[int] = []

    def __init__(self, seed: int, healthpoints: int, attack: int, defence: int, tower_levels: int, 
                 coins: int, difficulty: int, level_roads: int, level_depth: int) -> None:
        self.seed = seed
        self.brave = MagicUnit(healthpoints, attack, defence, coins)
        self.tower_levels = tower_levels
        self.difficulty = difficulty
        self.level_roads = level_roads
        self.level_depth = level_depth

    def setup(self):
        self.rng = np.random.RandomState(self.seed)
        self.score: int = 0
        return {'tower_levels': self.tower_levels}
    
    def run(self, sol):
        for level in range(self.tower_levels):
            level_map = self.build_level(level)
            sol.on_feedback(deepcopy(self.brave), deepcopy(level_map), deepcopy(self.level_depth), deepcopy(self.level_depth))
            potion_order, raid_order = sol.take_action()
            self.drinkpotion(potion_order)
            if self.raid_by_order(level, raid_order, level_map) is False:
                self.logger.info(f'Dead! Final score: {int(self.score)}')
                break
            self.logger.info(f'Next level! Current score: {int(self.score)}')
        self.SCORES.append(self.score)

    def on_action(self, action: Any) -> Any:
        return super().on_action(action)
    
    def build_level(self, level: int) -> List[List[MagicUnit]]:
        self.level_score: int = 0
        level_map: List[List["MagicUnit"]] = [[MagicUnit(0, 0, 0, 0)] * self.level_depth for _ in range(self.level_roads)]
        for i in range(self.level_roads):
            for j in range(self.level_depth):
                rng_coins: int = int(self.difficulty * self.rng.uniform(1, 2))
                unit_difficulty = rng_coins * (level + 1)
                rng_attributes = random_split(unit_difficulty, 3)
                rng_healthpoints = (len(rng_attributes[0]) + 1) * 100
                rng_attack = len(rng_attributes[1]) + 1
                rng_denfence = len(rng_attributes[2]) + 1
                level_map[i][j] = MagicUnit(rng_healthpoints, rng_attack, rng_denfence, int(rng_coins/4))
                self.level_score += unit_difficulty
        return level_map
    
    def drinkpotion(self, potion_order: List[int]):
        for i in range(POTION_CATEGORY):
            if self.brave.coins < potion_order[i]:
                potion_order[i] = self.brave.coins
            self.brave.coins -= potion_order[i]
        self.brave.drink_potion(MagicUnit(potion_order[0]*100, potion_order[1], potion_order[2], 0))

    def raid_by_order(self, level: int,  raid_order: List[int], level_map: List[List[MagicUnit]]) -> bool:
        roads_depth_now: List[int] = [0] * self.level_roads
        for i in raid_order:
            order = raid_order[i]
            if order < 0 or order > self.level_roads:
                continue
            attacked_mamono = level_map[order][roads_depth_now[order]]
            final_damage = self.brave.attack_mamono(attacked_mamono)
            self.brave.healthpoints -= final_damage
            self.brave.coins += attacked_mamono.coins
            if self.brave.healthpoints == 0:
                return False
            self.score += attacked_mamono.coins * (level + 1)
            roads_depth_now[order] += 1
            if roads_depth_now[order] is self.level_depth:
                self.score += self.level_score * (1 - float(i / (self.level_roads * self.level_depth)))
                return True
        return False
    
    @classmethod
    def show_results(cls):
        print('\nYour results:')
        print(f'Total scores: {int(sum(cls.SCORES))}')

    @classmethod
    def from_play_mode(cls) -> "MagicTower":
        return cls(healthpoints=1000, attack=10, defence=10, coins=10)

    @classmethod
    def get_interactive_player(cls):
        return InteractivePlayer
    
def random_split(n, m=3):
    gids = [np.random.randint(0, m) for i in range(n-3)]
    buckets = [[k for k in range(n-3) if gids[k] == i] for i in range(m)]
    return buckets