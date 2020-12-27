from abc import ABC, abstractmethod
from collections.abc import Callable


class AbstractClassifier(ABC):
    @abstractmethod
    def get_analyzer(self) -> Callable[[str], list[str]]:
        pass
