from typing import List, Tuple

import numpy as np


class Solution:
    """
    This is the baseline solution that takes random actions.
    """
    def setup(self, board: List[List[int]]):
        """
        Called once before the start of the game.
        :param board: 2D array of integers, -1 for unknown, 0 for empty, 1-8 for number of mines around
        """
        self._board = board
        self._n_rows = len(board)
        self._n_cols = len(board[0])
        self._rng = np.random.RandomState(0)
    
    def take_action(self) -> Tuple[int, int]:
        """
        Choose an action to take.
        :return: (x, y) position of the action
        """
        valid_positions = [(i, j) for i in range(self._n_rows) for j in range(self._n_cols) if self._board[i][j] == -1]
        return valid_positions[self._rng.choice(len(valid_positions))]

    def on_feedback(self, board: List[List[int]]):
        """
        Receive feedback from the environment after taking an action.
        :param board: 2D array of integers, -1 for unknown, 0 for empty, 1-8 for number of mines around
        """
        self._board = board
