import requests
import vkApi

baseUrl = "https://api.vk.com/method"
method = "users.getSubscriptions"

params = dict()
params["user_id"] = "32745906"
params["extended"] = "1"
params["access_token"] = "3342c69f3342c69f3342c69fda333696f8333423342c69f6c3d984fabfee196ccc6e826"
params["v"] = "5.124"

print(vkApi.get_request_string(method, params))
