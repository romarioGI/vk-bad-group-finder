import IOHelper
from classifierQualityReport import make_quality_report
from dataset import split_dataset
from logisticRegressionClassifier import LogisticRegressionClassifier


def list_to_tuple(lst):
    return lst[0], lst[1]


dataset = IOHelper.deserialize('dataset_True.json')
dataset = list_to_tuple(dataset)

train, test = split_dataset(dataset, 0.8)

cls = LogisticRegressionClassifier(train)

report = make_quality_report(cls, test)
print(report)
