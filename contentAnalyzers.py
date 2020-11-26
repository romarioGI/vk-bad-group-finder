def erotic_content_analyzer(group) -> list:
    if is_contain_words(group, ['порно', 'видео для взрослых']):
        return ['PORNO']
    return []


def opposition_content_analyzer(group) -> list:
    if is_contain_words(group, ['оппозиция', 'навальный']):
        return ['OPPOSITION']
    return []


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


class Classifier:
    def __init__(self, train_data: list):
        groups, types = __unzip_train_data(train_data)
        self.__clf = LogisticRegression()
        self.__clf.fit(groups, types)

    @staticmethod
    def __unzip_train_data(train_data: list):
        groups, types = [], []
        for (group, t) in train_data:
            groups.append(group)
            types.append(t)
        return groups, types
