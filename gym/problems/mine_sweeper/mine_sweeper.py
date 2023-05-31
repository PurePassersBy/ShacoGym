import time
from copy import deepcopy
from typing import Any, List, Tuple, Optional, Dict, cast

import numpy as np

from ..base import Environment


class InteractivePlayer:
    ...


class MineSweeper(Environment):
    MINE = -1
    EMPTY = 0

    RECORDS = []

    def __init__(self, n_rows: int, n_cols: int, n_mines: int, seed: int):
        assert n_rows > 0 and n_cols > 0 and n_mines > 0
        assert n_mines < n_rows * n_cols
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_mines = n_mines
        self.seed = seed

    def setup(self) -> Dict[str, Any]:
        self._rng = np.random.RandomState(self.seed)
        self._true_board = np.zeros(self.n_rows * self.n_cols, dtype=np.int32)
        self._true_board.flat[:self.n_mines] = self.MINE
        self._rng.shuffle(self._true_board)
        self._true_board = self._true_board.reshape(self.n_rows, self.n_cols)

        self._visible_board = np.full((self.n_rows, self.n_cols), -1, dtype=np.int32)
        self._visited_board = np.zeros((self.n_rows, self.n_cols), dtype=np.int8)

        self._remaining_empty = self.n_rows * self.n_cols - self.n_mines
        
        for i in range(self.n_rows):
            for j in range(self.n_rows):
                if self._true_board[i, j] == self.MINE:
                    self._add_mine(i, j)

        return {'board': deepcopy(self._visible_board.tolist())}

    def _add_mine(self, x: int, y: int):
        for i in range(max(0, x - 1), min(self.n_rows, x + 2)):
            for j in range(max(0, y - 1), min(self.n_cols, y + 2)):
                if self._true_board[i, j] != self.MINE:
                    self._true_board[i, j] += 1

    def run(self, sol):
        while True:
            action = sol.take_action()
            final_state = self.on_action(action)
            if final_state is not None:
                break
            sol.on_feedback(self._visible_board)
        if final_state:
            self.logger.info("You win!")
        else:
            self.logger.info("You lose!")
        self.RECORDS.append(final_state)

    def on_action(self, action: Tuple[int, int]) -> Optional[bool]:
        x, y = cast(Tuple[int, int], action)
        assert 0 <= x < self.n_rows and 0 <= y < self.n_cols
        self._visited_board[x, y] = 1
        self._remaining_empty -= 1
        if self._true_board[x, y] == self.MINE:
            return False
        elif self._true_board[x, y] == self.EMPTY:
            self._visible_board[x, y] = self.EMPTY
            for i in range(max(0, x - 1), min(self.n_rows, x + 2)):
                for j in range(max(0, y - 1), min(self.n_cols, y + 2)):
                    if self._visited_board[i, j] == 0 and self._true_board[i, j] != self.MINE:
                        is_player_win = self.on_action((i, j))
                        if is_player_win:
                            return True
        else:
            self._visible_board[x, y] = self._true_board[x, y]
        if self._remaining_empty == 0:
            return True
        return None

    @classmethod
    def show_results(cls):
        print('\nYour results:')
        print(f'Win rate: {int(sum(cls.RECORDS))}/{len(cls.RECORDS)}')

    @classmethod
    def from_play_mode(cls) -> "MineSweeper":
        return cls(n_rows=8, n_cols=8, n_mines=10, seed=int(time.time()))

    @classmethod
    def get_interactive_player(cls):
        return InteractivePlayer
