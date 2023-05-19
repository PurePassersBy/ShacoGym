from typing import Type

from .bandit import Bandit
from .tictactoe import TicTacToe
from .base import Environment


ENVIRONMENTS = {
    "bandit": Bandit,
    "tictactoe": TicTacToe,
}


def get_environment(name: str) -> Type[Environment]:
    env = ENVIRONMENTS.get(name)
    if env is None:
        raise ValueError(f"Unknown environment: {name}")
    return env
