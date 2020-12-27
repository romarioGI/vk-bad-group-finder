from abc import ABC, abstractmethod
from collections.abc import Callable


class AbstractClassifier(ABC):
    def get_analyzer(self) -> Callable[[dict], list[str]]:
        return lambda g: [self.predict(g)]

    @abstractmethod
    def predict(self, group_info: dict) -> str:
        pass
