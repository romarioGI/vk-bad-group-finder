import IOHelper
from classifierQualityReport import make_quality_report
from dataset import split_dataset
from logisticRegressionClassifier import LogisticRegressionClassifier

dataset = IOHelper.pickle_deserialize('dataset')

train, test = split_dataset(dataset, 0.8)

cls = LogisticRegressionClassifier(train)

# сохранять в файлы с расширением cls
IOHelper.pickle_serialize(cls, 'test.cls')
load_cls = IOHelper.pickle_deserialize('test.cls')

report = make_quality_report(load_cls, test)
print(report)
