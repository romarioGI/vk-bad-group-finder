from outputHelper import to_pretty
from task2 import Task2
from vkApiWrapper import VkApiWrapper
from contentAnalyzers import EroticContentAnalyzers, OppositionContentAnalyzers

vkApiWrapper = VkApiWrapper()

access_token = '7a754fc77a754fc77a754fc7627a004af177a757a754fc725cae7e2fe78c903c9fd8417'
task2 = Task2(access_token, [EroticContentAnalyzers(), OppositionContentAnalyzers()], vkApiWrapper)
user_id = vkApiWrapper.get_user_id(access_token, 'romarioGI')
res = task2.solve([user_id])
res = to_pretty(res)
print(res)
