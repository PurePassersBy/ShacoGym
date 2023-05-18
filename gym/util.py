import os
import importlib.util

import yaml

from typing import Any, Dict, List


def load_solution_from_file(file_path: os.PathLike[str]) -> type[Any]:
    spec = importlib.util.spec_from_file_location("solution", file_path)
    assert spec is not None and spec.loader is not None
    solution = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(solution)
    return solution.Solution


def load_problem_set(problem: str) -> Dict[str, Any]:
    def get_problem_set_file() -> str:
        return os.path.join(os.path.dirname(__file__), "problems", problem, "problem_set.yml")

    with open(get_problem_set_file(), "r") as f:
        return yaml.safe_load(f)