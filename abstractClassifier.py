from abc import ABC, abstractmethod
from collections.abc import Callable

OPPOSITE_TAG = 'opposite'
EROTIC_TAG = 'erotic'
OTHER_TAG = 'other'

ALL_TAGS = [OPPOSITE_TAG, EROTIC_TAG, OTHER_TAG]


def tag_to_num(tag: str):
    return ALL_TAGS.index(tag)


def num_to_tag(num: int):
    return ALL_TAGS[num]


class AbstractClassifier(ABC):
    def get_analyzer(self) -> Callable[[dict], list[str]]:
        def f(group):
            tag = self.predict(group)
            if tag == OTHER_TAG:
                return []
            return [f'{self.get_name()}-{tag}']

        return f

    @abstractmethod
    def predict(self, group_info: dict) -> int:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass
