from abc import ABC, abstractmethod
from typing import Any, Dict, Type


class Environment(ABC):
    def __init__(self, *args, **kwargs: Any) -> None:
        pass

    def set_logger(self, logger: Any) -> None:
        self.logger = logger

    # === Solve-Mode API ===
    @abstractmethod
    def run(self, sol: Any) -> None:
        pass

    @abstractmethod
    def setup(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def on_action(self, action: Any) -> Any:
        pass

    # === Play-Mode API ===
    @classmethod
    @abstractmethod
    def from_play_mode(cls) -> "Environment":
        pass

    @classmethod
    @abstractmethod
    def get_interactive_player(cls) -> Type:
        pass

    # === Evaluation API ===
    @classmethod
    @abstractmethod
    def show_results(cls) -> Any:
        pass

    # @classmethod
    # @abstractmethod
    # def from_file(cls, file_path: str) -> "Environment":
    #     pass

    # @classmethod
    # @abstractmethod
    # def show_baseline_results(cls) -> None:
    #     pass

    # @classmethod
    # @abstractmethod
    # def show_sota_results(cls) -> None:
    #     pass
