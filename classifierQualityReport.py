from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from abstractClassifier import AbstractClassifier, num_to_tag


def make_quality_report(classifier: AbstractClassifier, test_sample: (list[dict], list[int])):
    def tags_to_str(int_tags: list[int]):
        return [num_to_tag(t) for t in int_tags]

    groups, tags = test_sample
    predictions = [classifier.predict(g) for g in groups]

    tags = tags_to_str(tags)
    predictions = tags_to_str(predictions)

    res = f'accuracy:{accuracy_score(tags, predictions)}\n'
    res += f'{classification_report(tags, predictions)}\n'
    res += f'{confusion_matrix(tags, predictions)}'
    return res
