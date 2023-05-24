# Mine Sweeper

## Background

MineSweeper is a logic puzzle video game generally played on personal computers. The game features a grid of clickable squares, with hidden "mines" scattered throughout the board. The objective is to clear the board without detonating any mines, with help from clues about the number of neighboring mines in each field.

## Problem

You are given a $n\_rows\times n\_cols$ board, where $n\_mines$ mines hides. Every iteration, you are supposed to choose a cell which is denoted by a position tuple $(x, y)$ because you infer it is not mine. You get win if you clear the whole board without touching any mines.

## Template

```python
class Solution:
    """
        This is the Solution Template for mine_sweeper.
        Plz implemnt required functions below, while remain their interface unchanged.
    """
    def setup(self, board: List[List[int]]):
        """
        Called once before the start of the game.
        :param board: 2D array of integers, -1 for unknown, 0 for empty, 1-8 for number of mines around
        """
        raise NotImplementedError
    
    def take_action(self) -> Tuple[int, int]:
        """
        Choose an action to take.
        :return: (x, y) position of the action
        """
        raise NotImplementedError

    def on_feedback(self, board: List[List[int]]):
        """
        Receive feedback from the environment after taking an action.
        :param board: 2D array of integers, -1 for unknown, 0 for empty, 1-8 for number of mines around
        """
        raise NotImplementedError

```
