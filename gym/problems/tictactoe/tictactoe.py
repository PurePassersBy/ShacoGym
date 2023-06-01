import time
from copy import deepcopy
from typing import List, Optional, Tuple, Dict

import numpy as np

from ..base import Environment


class InteractivePlayer:
    def setup(self, marker: str, board: List[List[str]]) -> None:
        self.marker = marker
        self.board = board
        print('=== Welcome to ShacoGym. This is a Tic-Tac-Toe game. ===')
        print('In this game, two players take turns playing on a three-by-three board.\n\n'
              'One player plays "X"s and the other "O"s until one player wins by '
              'placing three marks in a row, horizontally, vertically, or diagonally.\n\n'
              'If the board fills up with neither player getting three in a row, then the game is a draw. "X" moves first.\n')
        print(f'=== You are playing as \"{marker}\" this time ===')
    
    def show_board(self) -> None:
        print('\nCurrent board:')
        for row in self.board:
            print(' '.join(row))

    def take_action(self, ) -> int:
        self.show_board()
        while True:
            action = input('Enter your action: ')
            if action.isdigit():
                action = int(action)
                if action in range(9) and self.board[action // 3][action % 3] == '_':
                    self.board[action // 3][action % 3] = self.marker
                    self.show_board()
                    return action
            print('Invalid action. Please try again.')
    
    def on_feedback(self, board: List[List[str]]) -> None:
        self.board = board


class TicTacToe(Environment):
    SIZE: int = 3
    VALID_MARKER = ['X', 'O']

    REWARDS: List[float] = []
    
    X_MAX_ACTIONS_MEMORY: Dict[int, Tuple[List[int], int]] = {}
    X_MIN_ACTIONS_MEMORY: Dict[int, Tuple[List[int], int]] = {}
    O_MAX_ACTIONS_MEMORY: Dict[int, Tuple[List[int], int]] = {}
    O_MIN_ACTIONS_MEMORY: Dict[int, Tuple[List[int], int]] = {}

    def __init__(self, seed: int, epsilon: float, marker: str) -> None:
        self.seed = seed
        self.epsilon = epsilon
        self.marker = marker
        self.opposite_marker = 'X' if marker == 'O' else 'O'

        self.max_actions_memory, self.min_actions_memory = (self.X_MAX_ACTIONS_MEMORY, self.X_MIN_ACTIONS_MEMORY) if marker == 'X' else \
                                                           (self.O_MAX_ACTIONS_MEMORY, self.O_MIN_ACTIONS_MEMORY)

    def setup(self):
        self.rng = np.random.RandomState(self.seed)
        self.board: List[List[str]] = [['_'] * self.SIZE for _ in range(self.SIZE)]
        self.reward: float = 0.

        if self.marker == 'X':
            self._step()
        
        return {'marker': self.opposite_marker, 'board': deepcopy(self.board)}

    def run(self, sol):
        while (final_state := not self._is_done()) is not None:
            action = sol.take_action()
            self.on_action(action)
            if (final_state := self._is_done()) is not None:
                break
            board = deepcopy(self.board)
            sol.on_feedback(board)
        
        if final_state == 'draw' or final_state == self.opposite_marker:
            self.reward = 1.

        self.REWARDS.append(self.reward)

        if final_state == self.marker:
            self.logger.info('You Lose!')
        elif final_state == self.opposite_marker:
            self.logger.info('You Win!')
        else:
            self.logger.info('Draw!')

    def on_action(self, action: int):
        assert action in range(self.SIZE ** 2)
        row, col = action // self.SIZE, action % self.SIZE
        assert self.board[row][col] == '_'
        self.board[row][col] = self.opposite_marker

        if not self._is_done():
            self._step()

    def _step(self):
        def _random_step() -> int:
            valid_actions = [i for i in range(self.SIZE ** 2) if self.board[i // self.SIZE][i % self.SIZE] == '_']
            action = self.rng.choice(valid_actions)
            return action

        if self.rng.random() < self.epsilon:  # take random action
            pos = _random_step()
        else:
            pos, _ = self._mini_max(True)
        
        self.board[pos // self.SIZE][pos % self.SIZE] = self.marker

    def _encode_board(self) -> int:
        code: int = 0
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                p = i * self.SIZE + j
                b = 0 if self.board[i][j] == '_' else (1 if self.board[i][j] == 'X' else 2)
                code += b ** p
        return code

    def _mini_max(self, is_max_turn: bool):
        final_status = self._is_done()
        if final_status == 'draw':
            return (-1, 0)
        elif final_status == self.marker:
            return (-1, 1)
        elif final_status == self.opposite_marker:
            return (-1, -1)

        code = self._encode_board()
        if is_max_turn and code in self.max_actions_memory:
            actions, score = self.max_actions_memory[code]
            return self.rng.choice(actions), score
        elif not is_max_turn and code in self.min_actions_memory:
            actions, score = self.min_actions_memory[code]
            return self.rng.choice(actions), score

        marker: str = self.marker if is_max_turn else self.opposite_marker
        best_score = (1 << 30) * (-1 if is_max_turn else 1)
        best_actions: List[int] = []
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.board[i][j] != '_':
                    continue
                self.board[i][j] = marker
                _, score = self._mini_max(is_max_turn ^ 1)
                self.board[i][j] = '_'
                
                action = i * self.SIZE + j
                if is_max_turn:
                    if score > best_score:
                        best_score, best_actions = score, [action]
                    elif score == best_score:
                        best_actions.append(action)
                else:
                    if score < best_score:
                        best_score, best_actions = score, [action]
                    elif score == best_score:
                        best_actions.append(action)
        if is_max_turn:
            self.max_actions_memory = (best_actions, best_score)
        else:
            self.min_actions_memory = (best_actions, best_score)
        return self.rng.choice(best_actions), best_score

    def _is_done(self, attempt_action: Optional[Tuple[int, str]]=None) -> Optional[str]:
        def _rewind():
            if attempt_action is not None:
                pos, _ = attempt_action
                row, col = pos // self.SIZE, pos % self.SIZE
                self.board[row][col] = '_'

        if attempt_action is not None:
            pos, marker = attempt_action
            row, col = pos // self.SIZE, pos % self.SIZE
            self.board[row][col] = marker
        # === check rows ===
        for row in self.board:
            if len(set(row)) == 1 and row[0] != '_':
                _rewind()
                return row[0]

        # === check columns ===
        for col in zip(*self.board):
            if len(set(col)) == 1 and col[0] != '_':
                _rewind()
                return col[0]

        # === check diagonals ===
        if len(set([self.board[i][i] for i in range(self.SIZE)])) == 1 and self.board[0][0] != '_':
            _rewind()
            return self.board[0][0]
        if len(set([self.board[i][self.SIZE - 1 - i] for i in range(self.SIZE)])) == 1 and self.board[0][self.SIZE - 1] != '_':
            _rewind()
            return self.board[0][self.SIZE - 1]

        # === check draw ===
        if all([cell != '_' for row in self.board for cell in row]):
            _rewind()
            return 'draw'

        _rewind()
        return None

    @classmethod
    def show_results(cls):
        print('\nYour results:')
        print(f'Win/Draw rate: {int(sum(cls.REWARDS))}/{len(cls.REWARDS)}')

    @classmethod
    def from_play_mode(cls) -> "TicTacToe":
        rng = np.random.RandomState(int(time.time()))
        marker = rng.choice(cls.VALID_MARKER)
        return cls(seed=0, epsilon=0.2, marker=marker)

    @classmethod
    def get_interactive_player(cls):
        return InteractivePlayer
