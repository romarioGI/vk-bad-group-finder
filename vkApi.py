import requests
import webbrowser


# TODO: всё равно в каждый метод нужна обработка ошибок и содержимого
# TODO: нужна асинхронность?
class VkApi:

    API_URI = "https://api.vk.com/method"
    API_VERSION = "5.124"
    CLIENT_ID = "7622759"  # vk app ID
    AUTHORIZE_URI = "https://oauth.vk.com"
    AUTHORIZE_REDIRECT_URI = "http://localhost"

    # TODO: протестировать что возвращает
    @staticmethod
    def __get_request(request: str):
        response = requests.get(request)
        return response.json()

    @staticmethod
    def __build_request_str(uri: str, method_name: str, params: dict) -> str:
        paramsString = "&".join(map(lambda p: f"{p[0]}={p[1]}", params.items()))
        return f"{uri}/{method_name}?{paramsString}"

    @classmethod
    def __api_request(cls, method_name: str, params: dict):
        request_str = cls.__build_request_str(cls.API_URI, method_name, params)
        return cls.__get_request(request_str)

    @classmethod
    def get_user_id(cls, screen_name: str, access_token: str):
        params = dict()
        params["screen_name"] = screen_name
        params["access_token"] = access_token
        method_name = "utils.resolveScreenName"
        return cls.__api_request(method_name, params)

    # TODO: паблики это подмножество групп? нужно пробовать написать метод,
    #  возвращающий пересечение множеств идшников групп и сообществ
    # оставить этот метод, так как группы могут быть закрыты, а паблики всегда открыты
    @classmethod
    def get_user_subscriptions(cls, user_id, access_token: str):
        params = dict()
        params["user_id"] = user_id
        params["extended"] = "0"
        params["access_token"] = access_token
        params["v"] = cls.API_VERSION
        method_name = "users.getSubscriptions"
        return cls.__api_request(method_name, params)

    # TODO: реализовать с учетом offset и того, что возвращается не более 1000 за раз
    # в count возвращается количество общее. Исходя из него можно понять какое смещение нужно.
    # или тупее: offset=i*1000, count=1000, while list_ids not empty
    @classmethod
    def get_user_groups(cls, user_id, access_token: str):
        params = dict()
        params["user_id"] = user_id
        params["extended"] = "0"
        params["access_token"] = access_token
        params["v"] = cls.API_VERSION
        method_name = "groups.get"
        return cls.__api_request(method_name, params)

    # TODO: разбиваем список групп на списки по 500 групп и делаем запрос groups.getById
    @classmethod
    def get_groups_information(cls, group_ids: list):
        pass

    # TODO: get user friends

    # scope flags constants
    __friends_scope = 1 << 1
    __offline_scope = 1 << 16
    __groups_scope = 1 << 18
    __scope = __friends_scope + __offline_scope + __groups_scope

    @classmethod
    def __build_get_access_token_request_str(cls) -> str:
        params = dict()
        params["client_id"] = cls.CLIENT_ID
        params["scope"] = cls.__scope
        params["response_type"] = "token"
        params["revoke"] = "1"
        params["v"] = cls.API_VERSION
        params["redirect_uri"] = cls.AUTHORIZE_REDIRECT_URI
        method = "authorize"
        request_str = cls.__build_request_str(cls.AUTHORIZE_URI, method, params)
        return request_str

    @classmethod
    def get_access_token(cls):
        request_str = cls.__build_get_access_token_request_str()
        """
        тут выбираем порт и начинаем его слушать
        """
        webbrowser.open(request_str)
        """
        тут сколько-то секунд ждем пока пользователь залогинится. если залогинился, то придет get запрос на порт
        с access_token, который мы вернём. иначе кидаем исключение
        """
