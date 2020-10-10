import requests

# TODO: брать их лучше из типа appconfig
# constants
baseUrl = "https://api.vk.com/method"
access_token = "3342c69f3342c69f3342c69fda333696f8333423342c69f6c3d984fabfee196ccc6e826"
api_version = "5.124"


def __request(methodName: str, params: dict):
    paramsString = "&".join(map(lambda p: p[0] + "=" + p[1], params.items()))
    request_str = baseUrl + "/" + methodName + "?" + paramsString
    return requests.get(request_str)


# TODO: паблики это подмножество групп? нужно пробовать написать метод,
#  возвращающий пересечение множеств идшников групп и сообществ
# TODO: вытащить из json id-ки групп
def get_user_subscriptions(user_id: str):
    params = dict()
    params["user_id"] = user_id
    params["extended"] = "0"
    params["access_token"] = access_token
    params["v"] = api_version
    method_name = "users.getSubscriptions"
    return __request(method_name, params)
