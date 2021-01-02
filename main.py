import IOHelper
from classifierQualityReport import make_quality_report
from dataset import split_dataset
from decisionTreeClassifier import DecisionTreeClassifier
from kNearestNeighboursClassifier import KNearestNeighboursClassifier
from logisticRegressionClassifier import LogisticRegressionClassifier
from randomForestClassifier import RndForestClassifier
from sagLogisticRegressionClassifier import SagLogisticRegressionClassifier
from task1 import Task1
from vkApiWrapper import VkApiWrapper, get_access_token
from vkAppConfigInfo import CLIENT_ID, CLIENT_SECRET
import abstractClassifier


def fit_and_serialize():
    data = IOHelper.pickle_deserialize('dataset')

    cls = KNearestNeighboursClassifier(data)
    IOHelper.pickle_serialize(cls, 'kNearestNeighboursClassifier.cls')

    cls = RndForestClassifier(data)
    IOHelper.pickle_serialize(cls, 'randomForestClassifier.cls')

    cls = DecisionTreeClassifier(data)
    IOHelper.pickle_serialize(cls, 'decisionTreeClassifier.cls')

    cls = SagLogisticRegressionClassifier(data)
    IOHelper.pickle_serialize(cls, 'sagLogisticRegressionClassifier.cls')

    cls = LogisticRegressionClassifier(data)
    IOHelper.pickle_serialize(cls, 'logisticRegressionClassifier.cls')


def demonstrate_fitting():
    dataset = IOHelper.pickle_deserialize('dataset')

    train, test = split_dataset(dataset, 0.75)

    cls = KNearestNeighboursClassifier(train)
    report = make_quality_report(cls, test)
    print(report)

    cls = RndForestClassifier(train)
    report = make_quality_report(cls, test)
    print(report)

    cls = DecisionTreeClassifier(train)
    report = make_quality_report(cls, test)
    print(report)

    cls = SagLogisticRegressionClassifier(train)
    report = make_quality_report(cls, test)
    print(report)

    cls = LogisticRegressionClassifier(train)
    report = make_quality_report(cls, test)
    print(report)


def main():
    user_names = ['id50440959']

    print('\rget token...', end='')
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)

    print('\rcreate wrapper...', end='')
    vk_api_wrapper = VkApiWrapper(access_token)

    print('\rget ids...', end='')
    user_ids = [vk_api_wrapper.get_user_id(s_n) for s_n in user_names]

    '''print('\rload decisionTree...', end='')
    decisionTree = IOHelper.pickle_deserialize('decisionTreeClassifier.cls').get_analyzer()'''
    print('\rload kNearestNeighbours...', end='')
    kNearestNeighbours = IOHelper.pickle_deserialize('kNearestNeighboursClassifier.cls').get_analyzer()
    print('\rload randomForestClassifier...', end='')
    '''randomForestClassifier = IOHelper.pickle_deserialize('randomForestClassifier.cls').get_analyzer()
    print('\rload sagLogisticRegressionClassifier...', end='')'''
    sagLogisticRegressionClassifier = IOHelper.pickle_deserialize('sagLogisticRegressionClassifier.cls').get_analyzer()
    print('\rload logisticRegressionClassifier...', end='')
    logisticRegressionClassifier = IOHelper.pickle_deserialize('logisticRegressionClassifier.cls').get_analyzer()

    print('\rconcat analyzers...', end='')
    # content_analyzers = [decisionTree, kNearestNeighbours, randomForestClassifier, sagLogisticRegressionClassifier,logisticRegressionClassifier]
    # content_analyzers = [kNearestNeighbours, sagLogisticRegressionClassifier, logisticRegressionClassifier]
    content_analyzers = [sagLogisticRegressionClassifier]

    print('\rcreate task1...', end='')
    task1 = Task1(content_analyzers, vk_api_wrapper)

    print('\rsolve...')
    result = task1.solve(user_ids)

    print(IOHelper.to_pretty(result))

    IOHelper.json_serialize(result, 'last_result.json', pretty=True)


main()
