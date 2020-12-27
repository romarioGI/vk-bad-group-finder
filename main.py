import time

from contentAnalyzers import erotic_content_analyzer, opposition_content_analyzer, get_ml_content_analyzer
from outputHelper import to_pretty
from task1 import Task1
from vkApiWrapper import VkApiWrapper

vkApiWrapper = VkApiWrapper()

# access_token = '7a754fc77a754fc77a754fc7627a004af177a757a754fc725cae7e2fe78c903c9fd8417'
access_token = vkApiWrapper.get_access_token('7669046', 'RaKr73JgXqP7NfR11VYM')

start_time = time.time()

use_extended_group_info = False
ml_content_analyzer = get_ml_content_analyzer(vkApiWrapper, access_token, use_extended_group_info)
print(time.time() - start_time)
analyzers = [erotic_content_analyzer, opposition_content_analyzer, ml_content_analyzer]

task1 = Task1(access_token, analyzers, vkApiWrapper)
user_id = vkApiWrapper.get_user_id(access_token, 'id50440959')
res = task1.solve([user_id], use_extended_group_info=use_extended_group_info)

res = to_pretty(res)
print(res)

print(time.time() - start_time)

# task1 с флагом use_extended_group_info=True на Семене Самарине работает порядка 271 секунды
