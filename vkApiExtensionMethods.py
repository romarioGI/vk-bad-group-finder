import random
import webbrowser
from threading import Thread, Lock

import requests

import vkApi
from authRequestRedirectServer import AuthRequestRedirectServer


class VkApiError(Exception):
    def __init__(self, error_response):
        self.error_code = error_response['error_code']
        self.error_msg = error_response['error_msg']
        self.request_params = error_response['request_params']
        message = f'{str(error_response)}\n see https://vk.com/dev/errors'
        super().__init__(message)


class VkApiResponse:
    def __init__(self, api_response: requests.Response):
        response = api_response.json()
        if 'error' in response:
            raise VkApiError(response['error'])
        elif 'response' in response:
            self.__response = response['response']
        else:
            raise Exception('wrong response format')
        if isinstance(self.response, dict):
            self.__is_object = True
        else:
            self.__is_object = False

    @property
    def is_empty(self):
        response = self.response
        return (isinstance(response, list) or isinstance(response, dict)) and len(response) == 0

    @property
    def response(self):
        return self.__response

    def __getitem__(self, attribute: str):
        if not self.__is_object:
            raise Exception('response is not object (dict) and does not have the any attributes')
        if attribute in self.response:
            return self.response[attribute]
        raise AttributeError(f'response does not have the {attribute} attribute')


class UserNotFound(Exception):
    def __init__(self, screen_name):
        super().__init__(f'user with {screen_name} not found')


class TimeoutExpiredError(Exception):
    def __init__(self, timeout):
        super().__init__(f'the timeout ({timeout}) has expired')


def get_user_id(access_token: str, screen_name: str) -> int:
    """
    https://vk.com/dev/utils.resolveScreenName
    """
    response = vkApi.get_utils_resolve_screen_name(access_token, screen_name)
    response = VkApiResponse(response)
    if response.is_empty:
        raise UserNotFound(screen_name)
    object_type = response['type']
    if object_type != 'user':
        raise UserNotFound(screen_name)
    object_id = response['object_id']
    return object_id


def __get_fields():
    fields = ['age_limits', 'description', 'main_album_id', 'status']
    return ','.join(fields)


# TODO: использовать wall.get, wall.search, video.get, мб через хранимые процедуры VK для оптимизации
def get_user_subscriptions(access_token: str, user_id) -> list:
    """
    https://vk.com/dev/users.getSubscriptions
    """
    fields = __get_fields()
    res = []
    while True:
        response = vkApi.get_user_subscriptions(access_token, user_id, 1, len(res), 200, fields)
        response = VkApiResponse(response)
        cur = response['items']
        res.extend(cur)
        if len(res) >= response['count']:
            break
    res = filter(
        lambda s: s['type'] in ['group', 'page', 'event'],
        res
    )
    return list(res)


def get_user_groups(access_token: str, user_id) -> list:
    """
    https://vk.com/dev/groups.get
    """
    fields = __get_fields()
    res = []
    while True:
        response = vkApi.get_user_groups(access_token, user_id, 1, None, fields, len(res), 1000)
        response = VkApiResponse(response)
        cur = response['items']
        res.extend(cur)
        if len(res) >= response['count']:
            break
    return res


def try_get_user_groups(access_token: str, user_id):
    try:
        groups = get_user_groups(access_token, user_id)
        return groups
    except VkApiError:
        subs = get_user_subscriptions(access_token, user_id)
        return subs


def get_friends(access_token: str, user_id):
    response = vkApi.get_friends(access_token, user_id, count=10000)
    response = VkApiResponse(response)
    return response['items']


def get_access_token(client_id, client_secret, port=None, timeout=60):
    """
    https://vk.com/dev/authcode_flow_user
    """

    def get_random_port():
        return random.randint(50000, 65000)

    def get_scope():
        friends_scope = 1 << 1
        video_scope = 1 << 4
        wall_scope = 1 << 13
        offline_scope = 1 << 16
        groups_scope = 1 << 18
        return friends_scope + video_scope + wall_scope + offline_scope + groups_scope

    def get_redirect_url():
        return f'http://{host}:{port}/vk_auth'

    def start_auth_server(callback):
        auth_server = AuthRequestRedirectServer(host, port, callback)
        thread = Thread(target=auth_server.run, daemon=True)
        thread.start()
        return auth_server

    def auth_callback(lock: Lock, output, answer: dict):
        for (key, value) in answer.items():
            output[key] = value
        lock.release()

    def open_browser():
        url = vkApi.build_get_access_code_request_str(client_id, redirect_uri, scope)
        webbrowser.open(url)

    def get_access_code():
        lock = Lock()
        output = dict()
        auth_server = start_auth_server(lambda answer: auth_callback(lock, output, answer))
        try:
            open_browser()

            lock.acquire()
            lock.acquire(timeout=timeout)
            lock.release()

            if len(output) == 0:
                raise TimeoutExpiredError(timeout)

            if 'code' in output:
                return output['code']
            raise Exception(f'{output}')
        finally:
            auth_server.stop()

    host = 'localhost'
    if port is None:
        port = get_random_port()
    redirect_uri = get_redirect_url()
    scope = get_scope()

    code = get_access_code()
    request_str = vkApi.build_get_access_token_request_str(client_id, client_secret, redirect_uri, code)
    response = requests.get(request_str).json()

    if 'access_token' in response:
        return response['access_token']
    raise Exception(str(response))
