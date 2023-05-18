from abc import ABC, abstractmethod
from typing import Any, Dict


class Environment(ABC):
    @abstractmethod
    def run(self, sol: Any) -> None:
        pass

    @abstractmethod
    def setup(self) -> Dict[str, Any]:
        pass

    def set_logger(self, logger: Any) -> None:
        pass

    @abstractmethod
    def on_action(self, action: Any) -> Any:
        pass

    @classmethod
    @abstractmethod
    def show_results(cls) -> Any:
        pass

    @classmethod
    @abstractmethod
    def from_file(cls, file_path: str) -> "Environment":
        pass

    @classmethod
    @abstractmethod
    def show_baseline_results(cls) -> None:
        pass

    @classmethod
    @abstractmethod
    def show_sota_results(cls) -> None:
        pass
