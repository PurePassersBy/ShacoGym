from typing import Type

from .bandit import Bandit
from .tictactoe import TicTacToe
from .magicTower import MagicTower
from .mine_sweeper import MineSweeper
from .base import Environment


ENVIRONMENTS = {
    "bandit": Bandit,
    "tictactoe": TicTacToe,
    "magicTower": MagicTower,
    "mine_sweeper": MineSweeper,
}


def get_environment(name: str) -> Type[Environment]:
    env = ENVIRONMENTS.get(name)
    if env is None:
        raise ValueError(f"Unknown environment: {name}")
    return env
