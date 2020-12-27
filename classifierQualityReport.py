from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from abstractClassifier import AbstractClassifier


def make_quality_report(classifier: AbstractClassifier, test_sample: list[dict], answers: list):
    predictions = [classifier.predict(g) for g in test_sample]
    res = f'accuracy:{accuracy_score(answers, predictions)}\n'
    res += f'{classification_report(answers, predictions)}\n'
    res += f'{confusion_matrix(answers, predictions)}'
    return res
