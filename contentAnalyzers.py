import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import firstDataset
from vkApiWrapper import VkApiWrapper


def erotic_content_analyzer(group) -> list:
    if is_contain_words(group, ['порн', 'видео для взрослых', 'эротик', 'пошл', 'porn', 'erotic']):
        return ['ADULT']
    return []


def opposition_content_analyzer(group) -> list:
    if is_contain_words(group, ['оппозиция', 'навальн', 'против путина', 'путин вор', 'корруп', 'митинг', 'пикет']):
        return ['POLITIC']
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
        for o in obj.keys():
            yield from __get_all_words(o)
        for o in obj.values():
            yield from __get_all_words(o)


class Classifier:
    def __init__(self, vkApiWrapper: VkApiWrapper, access_token: str, dataset: dict, use_extended_group_info: bool):
        groups_screen_names = list(dataset.keys())

        if use_extended_group_info:
            groups = vkApiWrapper.get_groups_extended_info(access_token, groups_screen_names)
        else:
            groups = vkApiWrapper.get_groups_info(access_token, groups_screen_names)

        groups_types = list(map(lambda g: dataset[g['screen_name']], groups))

        cv = CountVectorizer(analyzer='char', ngram_range=(3, 3), min_df=0.1, max_df=0.9)
        groups_info = list(map(lambda g: ''.join(self.__get_all_words(g)), groups))
        groups_info = cv.fit_transform(groups_info)

        clf = LogisticRegression(max_iter=300)
        clf.fit(groups_info, groups_types)

        self.__clf = clf
        self.__cv = cv

    @classmethod
    def __get_all_words(cls, obj):
        if isinstance(obj, str):
            yield re.sub(r'[^0-9а-яёa-z]+', '', obj.lower())
        elif isinstance(obj, list):
            for o in obj:
                yield from cls.__get_all_words(o)
        elif isinstance(obj, dict):
            for v in obj.values():
                yield from cls.__get_all_words(v)

    def predict(self, group_info):
        group_info = ''.join(self.__get_all_words(group_info))
        group_info = self.__cv.transform([group_info])
        pr = self.__clf.predict(group_info)
        return pr[0]

    @staticmethod
    def prediction_quality_report(answers, predictions) -> str:
        res = f'accuracy:{accuracy_score(answers, predictions)}\n'
        res += f'{classification_report(answers, predictions)}\n'
        res += f'{confusion_matrix(answers, predictions)}'
        return res


def get_ml_content_analyzer(vkApiWrapper: VkApiWrapper, access_token: str, use_extended_group_info: bool):
    classifier = Classifier(vkApiWrapper, access_token, firstDataset.dataset, use_extended_group_info)

    def f(group) -> list:
        tag = classifier.predict(group)
        if tag == firstDataset.non_tag:
            return []
        return [f'ML-{tag}']

    return f
