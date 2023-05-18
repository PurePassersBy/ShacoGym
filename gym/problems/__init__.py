from typing import Type

from .bandit import Bandit
from .base import Environment


ENVIRONMENTS = {
    "bandit": Bandit,
}


def get_environment(name: str) -> Type[Environment]:
    env = ENVIRONMENTS.get(name)
    if env is None:
        raise ValueError(f"Unknown environment: {name}")
    return env
