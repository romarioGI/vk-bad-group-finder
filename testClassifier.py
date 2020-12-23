from contentAnalyzers import Classifier
from firstDataset import opposite_tag, erotic_tag, non_tag, dataset
from vkApiWrapper import VkApiWrapper

vkApiWrapper = VkApiWrapper()
access_token = vkApiWrapper.get_access_token('7669046', 'RaKr73JgXqP7NfR11VYM')

use_extended_group_info = False
ml_content_classifier = Classifier(vkApiWrapper, access_token, dataset, False)

opposite_group_screen_names = ['kprf_oz', 'corrupcia_rf', 'club1528146', 'clublevayoppoziciy', 'newopposition_official',
                               'anticrisismeeting', 'realopposition']

erotic_group_screen_names = ['sexy_world_one', 'paradise_for_men_01', 'erotic_pics', 'seksualnye_modeli', 'nsk_models',
                             'eros_pub', 'erotica_so_vkusom']

non_group_screen_names = ['bad_novosti', 'tennissss', 'pod83', 'pikabu', 'mensrecipes', 'programmistov', 'for.mens',
                          'smexo', 'adkuhnya', 'nice_food', 'litrpg_book']

groups = opposite_group_screen_names + erotic_group_screen_names + non_group_screen_names
groups = vkApiWrapper.get_groups_info(access_token, groups)
answers = [opposite_tag] * len(opposite_group_screen_names) \
          + [erotic_tag] * len(erotic_group_screen_names) \
          + [non_tag] * len(non_group_screen_names)

predictions = list(map(lambda g: ml_content_classifier.predict(g), groups))

print(ml_content_classifier.prediction_quality_report(answers, predictions))
