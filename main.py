from outputHelper import to_pretty
from task1 import Task1
from vkApiWrapper import VkApiWrapper
from contentAnalyzers import EroticContentAnalyzers, OppositionContentAnalyzers

vkApiWrapper = VkApiWrapper()

access_token = vkApiWrapper.get_access_token('7669046', 'RaKr73JgXqP7NfR11VYM')
task1 = Task1(access_token, [EroticContentAnalyzers(), OppositionContentAnalyzers()], vkApiWrapper)
user_id = vkApiWrapper.get_user_id(access_token, 'romanalf')
res = task1.solve([user_id], ignore_private_accounts=False)
res = to_pretty(res)
print(res)
