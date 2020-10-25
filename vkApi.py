import requests
import webbrowser


# TODO метод для обращения к словарм, тип вместо d[key] try_get(d, key) если такого ключа нет
#  то кидать более исключения типа wrong json object. Или написать класс api response, чтоб в него
#  инкапсулировать все эти методы, в том числе обработку ошибок от VK
# TODO: указать где какой access_token применим в описании к методам
class VkApi:

    API_URI = 'https://api.vk.com/method'
    API_VERSION = '5.124'
    AUTHORIZE_URI = 'https://oauth.vk.com'

    @staticmethod
    def __get_request(request: str) -> dict:
        response = requests.get(request)
        return response.json()

    @staticmethod
    def __build_request_str(uri: str, method_name: str, params: dict) -> str:
        paramsString = '&'.join(map(lambda p: f'{p[0]}={p[1]}', params.items()))
        return f'{uri}/{method_name}?{paramsString}'

    # TODO: мб обрабатывать общие ошибки, не общие проталкивать дальше
    @classmethod
    def __api_request(cls, method_name: str, params: dict):
        request_str = cls.__build_request_str(cls.API_URI, method_name, params)
        return cls.__get_request(request_str)

    @classmethod
    def __get_utils_resolve_screen_name(cls, screen_name: str, access_token: str):
        params = dict()
        params['screen_name'] = screen_name
        params['access_token'] = access_token
        params['v'] = cls.API_VERSION
        method_name = 'utils.resolveScreenName'
        return cls.__api_request(method_name, params)

    # TODO: обработка ошибок
    @classmethod
    def get_user_id(cls, screen_name: str, access_token: str):
        response = cls.__get_utils_resolve_screen_name(screen_name, access_token)
        if 'error' in response:
            raise Exception
        response = response['response']
        if not isinstance(response, dict):
            raise Exception
        if response['type'] != 'user':
            raise Exception
        return response['object_id']

    # оставить этот метод, так как группы могут быть закрыты, а паблики всегда открыты
    @classmethod
    def __get_user_subscriptions(cls, user_id, access_token: str):
        params = dict()
        params['user_id'] = user_id
        params['extended'] = '0'
        params['access_token'] = access_token
        params['v'] = cls.API_VERSION
        method_name = 'users.getSubscriptions'
        return cls.__api_request(method_name, params)

    # TODO: обработка ошибок
    @classmethod
    def get_user_subscriptions(cls, user_id, access_token: str) -> list:
        response = cls.__get_user_subscriptions(user_id, access_token)
        if 'error' in response:
            raise Exception
        response = response['response']
        if not isinstance(response, dict):
            raise Exception
        return response['groups']['items']

    @classmethod
    def __get_user_groups(cls, user_id, access_token: str, offset: int):
        params = dict()
        params['user_id'] = user_id
        params['extended'] = '0'
        params['offset'] = offset
        params['count'] = 1000
        params['access_token'] = access_token
        params['v'] = cls.API_VERSION
        method_name = 'groups.get'
        return cls.__api_request(method_name, params)

    # TODO: обработка ошибок
    # TODO: быстро ли работает конкатенция списков
    # TODO: протестировать
    @classmethod
    def get_user_groups(cls, user_id, access_token: str):
        res = []
        offset = 0
        while True:
            response = cls.__get_user_groups(user_id, access_token, offset)
            if 'error' in response:
                raise Exception
            response = response['response']
            if not isinstance(response, dict):
                raise Exception
            res += response['items']
            offset = len(res)
            if offset >= response['count']:
                break
        return res

    # TODO get пересечение подписок и групп вроде равно просто группам, но группы чаще закрыты, чем подписки
    #  если гет групс выдаёт ошибку, то возвращаем только подписки
    @classmethod
    def get_user_groups_and_subscriptions(cls, user_id, access_token: str):
        pass

    # TODO: group_id -- это id или скрин нейм
    # TODO: проверка на то, что len(group_ids) <= 500. Добавить это в описание
    @classmethod
    def __get_groups_information(cls, access_token: str, group_ids: list = None, group_id=None, fields: list = None):
        params = dict()
        if group_ids is not None:
            params['group_ids'] = ','.join(group_ids)
        if group_id is not None:
            params['group_id'] = group_id
        if fields is not None:
            params['fields'] = ','.join(fields)
        params['access_token'] = access_token
        params['v'] = cls.API_VERSION
        method_name = 'groups.get'
        return cls.__api_request(method_name, params)

    # TODO: разбиваем список групп на списки по 500 (вынести в константу) групп и делаем __get_groups_information
    @classmethod
    def get_groups_information(cls, group_ids: list):
        pass

    @classmethod
    def get_group_information(cls, group_ids: list):
        pass

    # TODO: get user friends

    @classmethod
    def __build_get_access_token_request_str(cls, client_id, scope: int, authorize_redirect_uri: str) -> str:
        params = dict()
        params['client_id'] = client_id
        params['scope'] = scope
        params['response_type'] = 'token'
        params['revoke'] = '1'
        params['v'] = cls.API_VERSION
        params['redirect_uri'] = authorize_redirect_uri
        method = 'authorize'
        return cls.__build_request_str(cls.AUTHORIZE_URI, method, params)

    __AUTHORIZE_REDIRECT_URI_BASE = 'https://oauth.vk.com/blank.html'

    '''
    # scope flags constants
    __friends_scope = 1 << 1
    __offline_scope = 1 << 16
    __groups_scope = 1 << 18
    __scope = __friends_scope + __offline_scope + __groups_scope
    '''

    @classmethod
    def get_access_token(cls, client_id):
        authorize_redirect_uri = cls.__AUTHORIZE_REDIRECT_URI_BASE
        scope = (1 << 1) + (1 << 16) + (1 << 18)
        request_str = cls.__build_get_access_token_request_str(client_id, scope, authorize_redirect_uri)
        webbrowser.open(request_str)
        '''
        тут как-то нужно дождаться редиректа
        '''
        pass
