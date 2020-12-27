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
        return lambda g: [self.predict(g)]

    @abstractmethod
    def predict(self, group_info: dict) -> str:
        pass
