from task2 import Task2
import vkApiExtensionMethods
from vkApiRequestSender import VkApiRequestSender
from outputHelper import to_pretty


access_token = vkApiExtensionMethods.get_access_token('7669046', 'RaKr73JgXqP7NfR11VYM')


sender = VkApiRequestSender(2)
task2 = Task2(access_token, [], sender)

user_id = vkApiExtensionMethods.get_user_id(access_token, 'romarioGI')

res = task2.solve([user_id])
res = to_pretty(res)
print(res)
