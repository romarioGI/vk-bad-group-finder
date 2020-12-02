from contentAnalyzers import erotic_content_analyzer, opposition_content_analyzer, get_ml_content_analyzer
from outputHelper import to_pretty
from task1 import Task1
from vkApiWrapper import VkApiWrapper
import time

vkApiWrapper = VkApiWrapper()

#access_token = '7a754fc77a754fc77a754fc7627a004af177a757a754fc725cae7e2fe78c903c9fd8417'
access_token = vkApiWrapper.get_access_token('7669046', 'RaKr73JgXqP7NfR11VYM')

start_time = time.time()

task1 = Task1(access_token, [erotic_content_analyzer, opposition_content_analyzer,
                             get_ml_content_analyzer(vkApiWrapper, access_token)], vkApiWrapper)
user_id = vkApiWrapper.get_user_id(access_token, 'id64551742')
res = task1.solve([user_id])
res = to_pretty(res)
print(res)

print(time.time() - start_time)
