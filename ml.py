import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

from vkApiWrapper import VkApiWrapper


def train(y_train, X_train, y_test, X_test):
    cv = CountVectorizer(analyzer='char', ngram_range=(2, 3), min_df=0.1, max_df=0.9)

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


def __get_all_words(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, list):
        for o in obj:
            yield from __get_all_words(o)
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from __get_all_words(v)


vkApiWrapper = VkApiWrapper()
access_token = '7a754fc77a754fc77a754fc7627a004af177a757a754fc725cae7e2fe78c903c9fd8417'

opposite_group_screen_names = ['teamnavalny', 'gulag.media', 'navalny.group', 'navalny_live', 'vesna_democrat',
                               'maximkatz', 'club23017477', 'tvrain', 'club43854092', 'oppositionofrussia',
                               'limonov_eduard']
opposite_group_types = ['OPPOSITE'] * len(opposite_group_screen_names)

erotic_group_screen_names = ['tutsexx', 'posliye', 'pornobrazzersvk', 'nu_art_erotica',
                             'erotique_journal', 'ledesirerotique']
erotic_group_types = ['EROTIC'] * len(erotic_group_screen_names)

non_opposite_and_erotic_group_screen_names = ['yarchat', 'voprosi.svoya.igra', 'math.uniyar.contest',
                                              'yaroslavl_state_university', 'just_str', 'tproger', 'kuplinovplay',
                                              'cerceau', 'ctranno', 'pornopunk', 'solovievlive']
non_opposite_and_erotic_group_types = ['NON'] * len(non_opposite_and_erotic_group_screen_names)

groups_screen_names = opposite_group_screen_names + erotic_group_screen_names + non_opposite_and_erotic_group_screen_names
groups = vkApiWrapper.get_groups_info(access_token, groups_screen_names)
groups_info = list(map(lambda g: ''.join(__get_all_words(g)), groups))

groups_types = opposite_group_types + erotic_group_types + non_opposite_and_erotic_group_types

train_groups = vkApiWrapper.get_groups_info(access_token, ['derzkach', 'eroticheskie_gifki', 'sexliborg', 'olimpiprofi',
                                                           'citiesskylines', 'openyarru', 'navalnyclub',
                                                           'corrupcia_in_russia', 'rf_pravda'])
train_groups_info = list(map(lambda g: ''.join(__get_all_words(g)), train_groups))
train_groups_types = ['EROTIC', 'EROTIC', 'EROTIC', 'NON', 'NON', 'NON', 'OPPOSITE', 'OPPOSITE', 'OPPOSITE']

train(groups_types, groups_info, train_groups_types, train_groups_info)
