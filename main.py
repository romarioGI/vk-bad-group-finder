import IOHelper
from classifierQualityReport import make_quality_report
from dataset import split_dataset
from logisticRegressionClassifier import LogisticRegressionClassifier


def list_to_tuple(lst):
    return lst[0], lst[1]


dataset = IOHelper.json_deserialize('dataset_True.json')
dataset = list_to_tuple(dataset)

train, test = split_dataset(dataset, 0.8)

cls = LogisticRegressionClassifier(train)

# сохранять в файлы с расширением cls
IOHelper.pickle_serialize(cls, 'test.cls')
load_cls = IOHelper.pickle_deserialize('test.cls')

report = make_quality_report(load_cls, test)
print(report)
