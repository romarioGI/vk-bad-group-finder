import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from abstractClassifier import AbstractClassifier, num_to_tag


class FirstClassifier(AbstractClassifier):
    def get_name(self) -> str:
        return 'FirstClassifier'

    def __init__(self, dataset: (dict, int)):
        groups, tags = dataset

        groups_info = [self.__get_useful_info(g) for g in groups]

        cv = CountVectorizer(analyzer='char', ngram_range=(3, 3), min_df=0.1, max_df=0.9)
        groups_info = cv.fit_transform(groups_info)

        clf = LogisticRegression(max_iter=300)
        clf.fit(groups_info, tags)

        self.__clf = clf
        self.__cv = cv

    # TODO в attachments тоже есть полезная инфа
    @classmethod
    def __get_useful_info(cls, group) -> str:
        res = [group['name'], group['screen_name'], group['activity'], group['description'], group['status']]
        for p in group['wall']:
            res.append(p['text'])
        res = ''.join(res)
        return re.sub(r'[^0-9а-яёa-z]+', '', res.lower())

    def predict(self, group_info: dict) -> str:
        group_info = self.__get_useful_info(group_info)
        group_info = self.__cv.transform([group_info])
        pr = self.__clf.predict(group_info)
        return num_to_tag(pr[0])
