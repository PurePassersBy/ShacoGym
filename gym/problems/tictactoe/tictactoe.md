# Tic-Tac-Toe

## Background

Two players take turns playing on a three-by-three board. One player plays "X"s and the other "O"s until one player wins by placing three marks in a row, horizontally, vertically, or diagonally. If the board fills up with neither player getting three in a row, then the game is a draw. "X" moves first.

## Problem

It is easy to prove that a skilled player can play so as never to lose. In this problem, you are playing against an imperfect player, one whose play is sometimes incorrect and allows you to win. In every round of game, you get $1$ score if you win or draw, $0$ if you lose. Try your best to gain higher scores and take this problem as your first journey in ShacoGym!

## Template

```python
from typing import List

class Solution:
    """
        This is the Solution Template for tictactoe.
        Plz implemnt required functions below, while remain their interface unchanged.
    """
    def setup(self, marker: str, board: List[List[str]]) -> None:
        """
        Called once before the start of the game.
        @param marker: the marker of the agent, either 'X' or 'O'. 'X' moves first.
        @param board: the initial board state, a 3x3 matrix with each element being either 'X', 'O', or '_'.
        """
        raise NotImplementedError
    
    def take_action(self) -> int:
        """
        Choose an action to take.
        @return: the index of the action to take. row, col = index // 3, index % 3
        """
        raise NotImplementedError
    
    def on_feedback(self, board: List[List[str]]) -> None:
        """
        Receive feedback from the environment after taking an action.
        @param board: the current board state, a 3x3 matrix with each element being either 'X', 'O', or '_'.
        """
        raise NotImplementedError
```
