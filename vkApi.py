import requests

# constants
api_uri = "https://api.vk.com/method"
authorize_uri = "https://oauth.vk.com"
authorize_redirect_uri = "https://oauth.vk.com/blank.html"
api_version = "5.124"
client_id = "7622759"  # ID приложения


def __build_request_str(uri: str, method_name: str, params: dict) -> str:
    paramsString = "&".join(map(lambda p: p[0] + "=" + str(p[1]), params.items()))
    return uri + "/" + method_name + "?" + paramsString


def __api_request(method_name: str, params: dict):
    request_str = __build_request_str(api_uri, method_name, params)
    return requests.get(request_str)


# TODO: паблики это подмножество групп? нужно пробовать написать метод,
#  возвращающий пересечение множеств идшников групп и сообществ
# TODO: вытащить из json id-ки групп
# TODO: обработка ошибок
def get_user_subscriptions(user_id: str, access_token: str):
    params = dict()
    params["user_id"] = user_id
    params["extended"] = "0"
    params["access_token"] = access_token
    params["v"] = api_version
    method_name = "users.getSubscriptions"
    return __api_request(method_name, params)


# TODO: реализовать с учетом offset и того, что возвращается не более 1000 за раз
# в count возвращается количество общее. Исходя из него можно понять какое смещение нужно.
# или тупее: offset=i*1000, count=1000, while list_ids not empty
def get_user_groups(user_id: str, access_token: str):
    params = dict()
    params["user_id"] = user_id
    params["extended"] = "0"
    params["access_token"] = access_token
    params["v"] = api_version
    method_name = "groups.get"
    return __api_request(method_name, params)


# scope const
friends = 1 << 1
offline = 1 << 16
groups = 1 << 18
scope = friends + offline + groups


# TODO: нужно как-то не запрос отправить, а открыть браузер
def __build_get_access_token_request_str() -> str:
    params = dict()
    params["client_id"] = client_id
    params["redirect_uri"] = authorize_redirect_uri
    params["scope"] = scope
    params["response_type"] = "token"
    params["revoke"] = "1"
    params["v"] = api_version
    method = "authorize"
    request_str = __build_request_str(authorize_uri, method, params)
    return request_str
