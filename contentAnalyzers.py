class ContentAnalyzers:
    def __init__(self, tag: str, check_func):
        self.tag = tag
        self.check = check_func


class EroticContentAnalyzers(ContentAnalyzers):
    def __init__(self):
        super().__init__('PORN', self.__check)

    __bad_words = ['порно', 'видео для взрослых']

    @classmethod
    def __check(cls, group):
        return is_contain_words(group, cls.__bad_words)


class OppositionContentAnalyzers(ContentAnalyzers):
    def __init__(self):
        super().__init__('OPPOSITION', self.__check)

    __bad_words = ['оппозиция', 'навальный']

    @classmethod
    def __check(cls, group):
        return is_contain_words(group, cls.__bad_words)


def is_contain_words(obj, words: list):
    words = list(map(lambda w: w.lower(), words))
    return __is_contain_words(obj, words)


def __is_contain_words(obj, words: list):
    if isinstance(obj, str):
        s = obj.lower()
        for w in words:
            if s.find(w) != -1:
                return True
    elif isinstance(obj, list):
        for o in obj:
            if __is_contain_words(o, words):
                return True
    elif isinstance(obj, dict):
        for o in obj.values():
            if __is_contain_words(o, words):
                return True
    return False


def __get_all_words(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, list):
        for o in obj:
            yield from __get_all_words(o)
    elif isinstance(obj, dict):
        for o in obj.values():
            yield from __get_all_words(o)
