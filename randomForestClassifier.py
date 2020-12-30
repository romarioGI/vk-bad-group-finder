from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV

from abstractClassifier import AbstractClassifier


class RndForestClassifier(AbstractClassifier):
    def get_name(self) -> str:
        return 'Random1ForestClassifier'

    def __init__(self, dataset: (list[dict], list[int])):
        groups, tags = dataset

        groups_info = [AbstractClassifier.get_useful_info(g) for g in groups]

        cv = CountVectorizer(analyzer='char', ngram_range=(3, 3), min_df=0.1, max_df=0.9)
        groups_info = cv.fit_transform(groups_info)

        parameters = {'class_weight': ['balanced_subsample', 'balanced'], 'n_estimators': [110, 130],
                      'max_depth': [1, 7]}
        rnd_forest = RandomForestClassifier()
        rnd_forest_cv = GridSearchCV(rnd_forest, parameters)
        rnd_forest_cv.fit(groups_info, tags)
        print(rnd_forest_cv.best_params_)

        self.__clf = rnd_forest_cv
        self.__cv = cv

    def predict(self, group_info: dict) -> int:
        group_info = AbstractClassifier.get_useful_info(group_info)
        group_info = self.__cv.transform([group_info])
        pr = self.__clf.predict(group_info)
        return int(pr[0])
