import requests
import webbrowser
from vkApiResponse import VkApiResponse
from vkApiError import VkApiError
from vkApiEmptyResponseError import VkApiEmptyResponseError
from authRequestRedirectServer import AuthRequestRedirectServer
from threading import Lock, Thread


class VkApi:
    API_URI = 'https://api.vk.com/method'
    API_VERSION = '5.124'
    AUTHORIZE_URI = 'https://oauth.vk.com'

    @staticmethod
    def __build_request_str(uri: str, method_name: str, params: dict) -> str:
        paramsString = '&'.join(map(lambda p: f'{p[0]}={p[1]}', params.items()))
        return f'{uri}/{method_name}?{paramsString}'

    @classmethod
    def __api_request(cls, method_name: str, params: dict) -> VkApiResponse:
        params['v'] = cls.API_VERSION
        request_str = cls.__build_request_str(cls.API_URI, method_name, params)
        return VkApiResponse(requests.get(request_str))

    @classmethod
    def __get_utils_resolve_screen_name(cls, screen_name: str, access_token: str) -> VkApiResponse:
        """
        see <a href=https://vk.com/dev/utils.resolveScreenName>link<a/>
        """
        params = dict()
        params['screen_name'] = screen_name
        params['access_token'] = access_token
        method_name = 'utils.resolveScreenName'
        return cls.__api_request(method_name, params)

    @classmethod
    def get_user_id(cls, screen_name: str, access_token: str) -> str:
        """
        see <a href=https://vk.com/dev/utils.resolveScreenName>link<a/>
        """
        response = cls.__get_utils_resolve_screen_name(screen_name, access_token)
        if response.is_empty:
            raise VkApiEmptyResponseError
        object_type = response['type']
        if object_type != 'user':
            raise Exception(f'{screen_name} is not user name, it is {object_type} name')
        object_id = response['object_id']
        return object_id

    # оставить этот метод, так как группы могут быть закрыты, а паблики всегда открыты
    @classmethod
    def __get_user_subscriptions(cls, user_id, access_token: str) -> VkApiResponse:
        """
        see <a href=https://vk.com/dev/users.getSubscriptions>link<a/>
        """
        params = dict()
        params['user_id'] = user_id
        params['extended'] = '0'
        params['access_token'] = access_token
        method_name = 'users.getSubscriptions'
        return cls.__api_request(method_name, params)

    @classmethod
    def get_user_subscriptions(cls, user_id, access_token: str) -> list:
        """
        see <a href=https://vk.com/dev/users.getSubscriptions>link<a/>
        """
        response = cls.__get_user_subscriptions(user_id, access_token)
        return response['groups']['items']

    @classmethod
    def __get_user_groups(cls, user_id, access_token: str, offset: int) -> VkApiResponse:
        """
        see <a href=https://vk.com/dev/groups.get>link<a/>
        """
        params = dict()
        params['user_id'] = user_id
        params['extended'] = '0'
        params['offset'] = offset
        params['count'] = 1000
        params['access_token'] = access_token
        method_name = 'groups.get'
        return cls.__api_request(method_name, params)

    @classmethod
    def get_user_groups(cls, user_id, access_token: str) -> list:
        """
        see <a href=https://vk.com/dev/groups.get>link<a/>
        """
        res = []
        while True:
            response = cls.__get_user_groups(user_id, access_token, len(res))
            res.extend(response['items'])
            if len(res) >= response['count']:
                break
        return res

    @classmethod
    def get_user_groups_or_subscriptions(cls, user_id, access_token: str) -> list:
        try:
            groups = cls.get_user_groups(user_id, access_token)
            return groups
        except VkApiError:
            subs = cls.get_user_subscriptions(user_id, access_token)
            return subs

    @classmethod
    def __get_groups_information(cls, access_token: str, group_ids: list, fields: list = None) -> VkApiResponse:
        """
        see <a href=https://vk.com/dev/groups.getById>link<a/>
        """
        params = dict()
        params['group_ids'] = ','.join(group_ids)
        if fields is not None:
            params['fields'] = ','.join(fields)
        params['access_token'] = access_token
        method_name = 'groups.getById'
        return cls.__api_request(method_name, params)

    MAX_GROUP_IDS_COUNT = 500

    @classmethod
    def get_groups_information(cls, access_token: str, group_ids: list):
        res = []
        for i in range(0, len(group_ids), cls.MAX_GROUP_IDS_COUNT):
            groups_info = cls.__get_groups_information(access_token, group_ids[i:i + cls.MAX_GROUP_IDS_COUNT])
            res.extend(groups_info.response)
        return res

    # TODO: переписать, так как этот метод мало даёт
    #   для анализа пригодятся name, screen_name, activity, age_limits, description, status,
    #   wall.get, wall.search, video.get,
    @classmethod
    def get_group_information(cls, access_token: str, group_id):
        return cls.get_groups_information(access_token, [group_id])

    @classmethod
    def __get_friends(cls, access_token: str, user_id) -> VkApiResponse:
        """
        see <a href=https://vk.com/dev/friends.get>link<a/>
        """
        params = dict()
        params['user_id'] = user_id
        params['access_token'] = access_token
        method_name = 'friends.get'
        return cls.__api_request(method_name, params)

    @classmethod
    def get_friends(cls, access_token: str, user_id) -> list:
        """
        see <a href=https://vk.com/dev/friends.get>link<a/>
        """
        response = cls.__get_friends(access_token, user_id)
        return response['items']

    @classmethod
    def __build_get_access_code_request_str(cls, client_id, scope: int, authorize_redirect_uri: str) -> str:
        """
        see <a href=https://vk.com/dev/authcode_flow_user>link<a/>
        """
        params = dict()
        params['client_id'] = client_id
        params['scope'] = scope
        params['response_type'] = 'code'
        params['revoke'] = '1'
        params['redirect_uri'] = authorize_redirect_uri
        method = 'authorize'
        return cls.__build_request_str(cls.AUTHORIZE_URI, method, params)

    @classmethod
    def __build_get_access_token_request_str(cls, client_id, client_secret, authorize_redirect_uri: str, code) -> str:
        """
        see <a href=https://vk.com/dev/authcode_flow_user>link<a/>
        """
        params = dict()
        params['client_id'] = client_id
        params['client_secret'] = client_secret
        params['redirect_uri'] = authorize_redirect_uri
        params['code'] = code
        method = 'access_token'
        return cls.__build_request_str(cls.AUTHORIZE_URI, method, params)

    __AUTHORIZE_REDIRECT_HOST = 'localhost'
    __friends_scope = 1 << 1
    __video_scope = 1 << 4
    __wall_scope = 1 << 13
    __offline_scope = 1 << 16
    __groups_scope = 1 << 18
    __scope = __friends_scope + __video_scope + __wall_scope + __offline_scope + __groups_scope

    @classmethod
    def get_access_token(cls, client_id, client_secret, port=8880):
        """
        see <a href=https://vk.com/dev/authcode_flow_user>link<a/>
        """
        host = cls.__AUTHORIZE_REDIRECT_HOST
        authorize_redirect_uri = f'http://{host}:{port}/vk_auth'
        scope = cls.__scope

        code = cls.__get_access_code(client_id, host, port, authorize_redirect_uri, scope)
        request_str = cls.__build_get_access_token_request_str(client_id, client_secret, authorize_redirect_uri, code)
        re = requests.get(request_str).json()

        if 'access_token' in re:
            return re['access_token']
        raise Exception(str(re))

    @classmethod
    def __get_access_code(cls, client_id, host, port, authorize_redirect_uri, scope, timeout=60):
        lock = Lock()
        lock.acquire()
        auth_server = AuthRequestRedirectServer(host, port, lock)
        thread = Thread(target=auth_server.run, daemon=True)
        thread.start()

        request_str = cls.__build_get_access_code_request_str(client_id, scope, authorize_redirect_uri)
        webbrowser.open(request_str)
        lock.acquire(timeout=timeout)
        lock.release()

        output = auth_server.output
        del thread
        del auth_server

        if output is None:
            raise Exception(f'the timeout ({timeout}) has expired')

        if 'code' in output:
            return output['code']
        raise Exception(f'{output}')
