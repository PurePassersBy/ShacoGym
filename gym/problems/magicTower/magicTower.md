# Magic Tower

## Background

Have you ever played the game "Magic Tower". As a Breave, you must go to the top of magic tower to save the princess. But there's no princesses in the tower, you goal is to get the highest score as you can! Here are the rules.  
1. Each level has several roads, you have to walk through a road to get to the next level. And you can switch roads at will.
2. Each road has several mamonos. Defeat mamonos will give you coins. When you reach the next level, you will get a chance to use coins to buy potions.
3. You and mamonos have the following three attributes: `HealthPoint`, `Attack` and `Defence`. As you know, `Damage = Attack - Defence`. If you Attack is lower than the mamono's defense, you can't defeat it.
4. When you defeat mamonos and go to the next level, you will earn score. So you can balance defeat mamonos and climb tower to get higher score.

## Tempalte

```python
class MagicUnit:
    """
    Your barve and mamonos are made up of it.
    """
    def __init__(self, healthpoints: int, attack: int, defence: int, coins: int) -> None:
        self.healthpoints = healthpoints
        self.attack = attack
        self.defence = defence
        self.coins = coins
    
    def attack_mamono(self, mamono: "MagicUnit") -> int:
        """
        Testing attck mamono.
        @param mamono: the attacked mamono.
        @return final_damage: the damage you will suffer, if you attack the mamono.
        """
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
        @param tower_levels: the tower's total levels.
        """
        raise NotImplementedError
    
    def take_action(self):
        """
        Choose an action to take.
        @return potion_order: the list of potions order. One conin can buy 100 healthpoints, 1 attack or 1 defence. The list is [healthpoints, attack, defence].
        @return raid_order: the list of raid order, which stores road number(0, 1, 2, 3, ect). If num < 0 or num >= level_roads, we will ignore the action. If you donn't walk to the end of one of the road, you will die. Which means the number of choices for one of the roads must to be greater than n.
        """
        raise NotImplementedError
    
    def on_feedback(self, brave: MagicUnit, level_map: List[List[MagicUnit]], level_roads: int, level_depth: int) -> None:
        """
        Receive feedback from the environment after taking an action.
        @param brave: it's your brave!
        @param level_map: the map of current level. It's a two-dimensional array, which full of mamonos.
        @param level_roads: the number of roads.
        @param level_roads: the depth of roads.
        """
        raise NotImplementedError
```