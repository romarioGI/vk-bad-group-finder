import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from vkApiWrapper import VkApiWrapper


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
    def __init__(self, vkApiWrapper: VkApiWrapper, access_token: str):
        opposite_group_screen_names = ['teamnavalny', 'gulag.media', 'navalny.group', 'navalny_live', 'vesna_democrat',
                                       'maximkatz', 'club23017477', 'tvrain', 'club43854092', 'oppositionofrussia',
                                       'limonov_eduard', 'navalnyclub', 'corrupcia_in_russia', 'rf_pravda']
        opposite_group_types = ['OPPOSITE'] * len(opposite_group_screen_names)

        erotic_group_screen_names = ['tutsexx', 'posliye', 'pornobrazzersvk', 'nu_art_erotica',
                                     'erotique_journal', 'ledesirerotique', 'derzkach', 'eroticheskie_gifki',
                                     'sexliborg']
        erotic_group_types = ['EROTIC'] * len(erotic_group_screen_names)

        non_opposite_and_erotic_group_screen_names = ['yarchat', 'voprosi.svoya.igra', 'math.uniyar.contest',
                                                      'yaroslavl_state_university', 'just_str', 'tproger',
                                                      'kuplinovplay', 'olimpiprofi', 'citiesskylines', 'openyarru',
                                                      'cerceau', 'ctranno', 'pornopunk', 'solovievlive']
        non_opposite_and_erotic_group_types = ['NON'] * len(non_opposite_and_erotic_group_screen_names)

        groups_screen_names = opposite_group_screen_names + erotic_group_screen_names + non_opposite_and_erotic_group_screen_names
        groups = vkApiWrapper.get_groups_info(access_token, groups_screen_names)

        groups_info = list(map(lambda g: ''.join(self.__get_all_words(g)), groups))
        groups_types = opposite_group_types + erotic_group_types + non_opposite_and_erotic_group_types

        cv = CountVectorizer(analyzer='char', ngram_range=(2, 3), min_df=0.1, max_df=0.9)

        groups_info = map(lambda text: re.sub(r'[^0-9А-яЁёa-zA-Z]+', '', text), groups_info)
        groups_info = cv.fit_transform(groups_info)

        clf = LogisticRegression()
        clf.fit(groups_info, groups_types)
        self.__clf = clf
        self.__cv = cv

    @classmethod
    def __get_all_words(cls, obj):
        if isinstance(obj, str):
            yield obj
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


def get_ml_content_analyzer(vkApiWrapper: VkApiWrapper, access_token: str):
    classifier = Classifier(vkApiWrapper, access_token)

    def f(group):
        return [f'ML-{classifier.predict(group)}']

    return f
