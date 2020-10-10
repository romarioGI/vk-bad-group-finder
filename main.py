import requests
import vkApi

print(vkApi.get_user_subscriptions("1889345").content)
