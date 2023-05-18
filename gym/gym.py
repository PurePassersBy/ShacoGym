import os
import logging
from typing import Any, List, Dict

from .problems import get_environment
from .util import (
    load_solution_from_file,
    load_problem_set,
)


class Gym:
    """
    Next Generation Competitive Programming Platform
    """
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    def run(self, problem_name: str, solution_file: os.PathLike[str]) -> None:
        # === import problem environment ===
        try:
            env_cls = get_environment(problem_name)
        except ValueError as e:
            self.logger.error(e)
            return

        # === import solution ===
        try:
            sol_cls = load_solution_from_file(solution_file)
        except Exception as e:
            self.logger.error(e)
            return

        # === run ===
        problem_set = load_problem_set(problem_name)
        test_cases: List[Dict[str, Any]] = problem_set["test_cases"]
        self.logger.info(f'Start to run {problem_name} problem with {len(test_cases)} test cases.')
        for i, problem_case in enumerate(test_cases):
            self.logger.info(f"\nRunning case: {i + 1} / {len(test_cases)}")
            env = env_cls(**problem_case)
            env.set_logger(self.logger)
            sol = sol_cls()
            env_setup_info = env.setup()
            sol.setup(**env_setup_info)
            env.run(sol)
            # self.logger.info(f"Results: {env.get_results()}")

        env_cls.show_results()
        # env_cls.show_baseline_results()
        # env_cls.show_sota_results()
        print('You can compare your result with Baseline and SOTA. Have a fun!')
