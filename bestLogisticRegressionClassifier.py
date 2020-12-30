from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

from abstractClassifier import AbstractClassifier


class BestLogisticRegressionClassifier(AbstractClassifier):
    def get_name(self) -> str:
        return 'BestLogisticRegressionClassifier'

    def __init__(self, dataset):
        groups, tags = dataset

        groups_info = [AbstractClassifier.get_useful_info(g) for g in groups]

        cv = CountVectorizer(analyzer='char', ngram_range=(3, 3), min_df=0.1, max_df=0.9)
        groups_info = cv.fit_transform(groups_info)

        parameters = {'solver': ['liblinear', 'saga', 'sag', 'lbfgs', 'newton-cg'], 'random_state': [20, 35],
                      'max_iter': [290, 300]}
        log_reg = LogisticRegression()
        log_reg_cv = GridSearchCV(log_reg, parameters)
        log_reg_cv.fit(groups_info, tags)
        print(log_reg_cv.best_params_)
        self.__clf = log_reg_cv
        self.__cv = cv

    def predict(self, group_info: dict) -> int:
        group_info = AbstractClassifier.get_useful_info(group_info)
        group_info = self.__cv.transform([group_info])
        pr = self.__clf.predict(group_info)
        return int(pr[0])
