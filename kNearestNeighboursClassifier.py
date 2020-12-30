from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

from abstractClassifier import AbstractClassifier


class KNearestNeighboursClassifier(AbstractClassifier):
    def get_name(self) -> str:
        return 'KNearestNeighboursClassifier'

    def __init__(self, dataset: (list[dict], list[int])):
        groups, tags = dataset

        groups_info = [AbstractClassifier.get_useful_info(g) for g in groups]

        cv = CountVectorizer(analyzer='char', ngram_range=(3, 3), min_df=0.1, max_df=0.9)
        groups_info = cv.fit_transform(groups_info)

        parameters = {'weights': ['uniform', 'distance'], 'n_neighbors': [3, 9], 'leaf_size': [20, 35]}
        k_neighbors = KNeighborsClassifier()
        k_neighbors_cv = GridSearchCV(k_neighbors, parameters)
        k_neighbors_cv.fit(groups_info, tags)
        print(k_neighbors_cv.best_params_)

        self.__clf = k_neighbors_cv
        self.__cv = cv

    def predict(self, group_info: dict) -> int:
        group_info = AbstractClassifier.get_useful_info(group_info)
        group_info = self.__cv.transform([group_info])
        pr = self.__clf.predict(group_info)
        return int(pr[0])
