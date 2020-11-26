import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix


def train(y_train, X_train, y_test, X_test):
    cv = CountVectorizer(analyzer='char', ngram_range=(3, 3), min_df=0.1, max_df=0.9)

    X_train = map(lambda text: re.sub(r'[^0-9А-яЁёa-zA-Z]+', '', text), X_train)
    X_train = cv.fit_transform(X_train)

    X_test = map(lambda text: re.sub(r'[^0-9А-яЁёa-zA-Z]+', '', text), X_test)
    X_test = cv.transform(X_test)

    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    calc_method(y_test, y_pred)


def calc_method(y_test, y_pred):
    print("accuracy:", accuracy_score(y_test, y_pred))
    print("f1_score:", f1_score(y_test, y_pred, average="weighted"))
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))


X_train = ['11 156 4658 13', '44 566 989 133 646 789', '465465465', '24234235252', '24342352352', '5252 52245 252',
           'qewqeqwdq', 'qw fff jjj', 'iii m l', 'ddfgdfg dfdfgd wadadhrg', 'dawdawdg fwfewfw fwfewf fwef',
           'dqwdqwqwdqwd',
           'а м п паа', 'вфцв ф', 'фмиер кек е', 'вйцвцйвйц', 'йцуй йуйцвфв афцафац афацф', 'пыупыуаыуа']
y_train = [0, 0, 0, 0, 0, 0,
           1, 1, 1, 1, 1, 1,
           2, 2, 2, 2, 2, 2]
X_test = ['45664', 'dsfsf', 'аа раа она']
y_test = [0, 1, 2]

train(y_train, X_train, y_test, X_test)

opposite_group_screen_names = ['teamnavalny', 'gulag.media', 'navalny.group', 'navalny_live', 'vesna_democrat',
                               'maximkatz', 'club23017477', 'tvrain', 'club43854092']

non_opposite_and_erotic_group_screen_names = ['yarchat', 'voprosi.svoya.igra', 'math.uniyar.contest',
                                              'yaroslavl_state_university', 'just_str', 'tproger', 'kuplinovplay']
