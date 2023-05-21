import numpy as np

from typing import List


class Solution:
    SIZE = 3

    def setup(self, marker: str, board: List[List[str]]) -> None:
        """
        Called once before the start of the game.
        @param marker: the marker of the agent, either 'X' or 'O'. 'X' moves first.
        @param board: the initial board state, a 3x3 matrix with each element being either 'X', 'O', or '_'.
        """
        self.marker = marker
        self.board = board
        self.rng = np.random.default_rng(0)
    
    def take_action(self) -> int:
        """
        Choose an action to take.
        @return: the index of the action to take. row, col = index // 3, index % 3
        """
        return self.random_step()
        
    def random_step(self) -> int:
        valid_actions = [i for i in range(self.SIZE ** 2) if self.board[i // self.SIZE][i % self.SIZE] == '_']
        action = self.rng.choice(valid_actions)
        return action
    
    def on_feedback(self, board: List[List[str]]) -> None:
        """
        Receive feedback from the environment after taking an action.
        @param board: the current board state, a 3x3 matrix with each element being either 'X', 'O', or '_'.
        """
        self.board = board
