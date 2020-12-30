import re
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
    def get_analyzer(self) -> Callable[[dict], str]:
        def f(group):
            tag = self.predict(group)
            tag = num_to_tag(tag)
            if tag == OTHER_TAG:
                return None
            return f'{tag}-{self.get_name()}'

        return f

    @abstractmethod
    def predict(self, group_info: dict) -> int:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @classmethod
    def get_useful_info(cls, group) -> str:
        res = cls.__get_useful_info(group)
        res = ''.join(res)
        return re.sub(r'[^0-9а-яёa-z]+', '', res.lower())

    __USEFUL_KEYS = ['description', 'text', 'title']

    @classmethod
    def __get_useful_info(cls, group: dict):
        def get_values_for_keys(obj):
            if isinstance(obj, dict):
                for k in cls.__USEFUL_KEYS:
                    if k in obj and isinstance(obj[k], str):
                        yield obj[k]
                for v in obj.values():
                    yield from get_values_for_keys(v)
            if isinstance(obj, list):
                for i in obj:
                    yield from get_values_for_keys(i)

        groups_keys = ['name', 'screen_name', 'activity', 'status']
        for k_ in groups_keys:
            if k_ in group:
                yield group[k_]
        yield from get_values_for_keys(group)
