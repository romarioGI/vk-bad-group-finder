from task2 import Task2
from vkApiWrapper import VkApiWrapper
from outputHelper import to_pretty

vkApiWrapper = VkApiWrapper()

access_token = vkApiWrapper.get_access_token('7669046', 'RaKr73JgXqP7NfR11VYM')
task2 = Task2(access_token, [], vkApiWrapper)
user_id = vkApiWrapper.get_user_id(access_token, 'romarioGI')
res = task2.solve([user_id], ignore_private_accounts=False)
res = to_pretty(res)
print(res)