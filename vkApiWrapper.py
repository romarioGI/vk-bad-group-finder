import random
import webbrowser
from collections.abc import Callable
from threading import Thread, Lock

import requests

import vkApi
from authRequestRedirectServer import AuthRequestRedirectServer
from vkApiError import VkApiError
from vkApiRequestSender import VkApiRequestSender
from vkApiResponse import VkApiResponse


class UserNotFound(Exception):
    def __init__(self, screen_name):
        super().__init__(f'user with {screen_name} not found')


class VkApiWrapper:
    def __init__(self, access_token: str, request_attempts_number: int = 2, request_per_second_limit: int = 3):
        self.__access_token = access_token
        self.__sender = VkApiRequestSender(request_attempts_number, request_per_second_limit)

    def __send(self, api_request_func: Callable[[...], requests.Response], **params) -> VkApiResponse:
        def f():
            response = api_request_func(**params)
            return VkApiResponse(response)

        return self.__sender.send(f)

    def get_user_id(self, screen_name: str) -> int:
        """
        https://vk.com/dev/utils.resolveScreenName
        """
        response = self.__send(vkApi.get_utils_resolve_screen_name, access_token=self.__access_token,
                               screen_name=screen_name)
        if response.is_empty:
            raise UserNotFound(screen_name)
        object_type = response['type']
        if object_type != 'user':
            raise UserNotFound(screen_name)
        object_id = response['object_id']
        return object_id

    def get_user_subscription_ids(self, user_id) -> list:
        """
        https://vk.com/dev/users.getSubscriptions
        """
        response = self.__send(vkApi.get_user_subscriptions, access_token=self.__access_token, user_id=user_id,
                               extended=0)
        res = response['groups']['items']
        return res

    def get_user_group_ids(self, user_id) -> list:
        """
        https://vk.com/dev/groups.get
        """
        res = []
        while True:
            response = self.__send(vkApi.get_user_groups, access_token=self.__access_token, user_id=user_id, extended=0,
                                   offset=len(res), count=1000)
            cur = response['items']
            res.extend(cur)
            if len(res) >= response['count']:
                break
        return res

    def try_get_user_group_ids(self, user_id) -> list:
        try:
            groups = self.get_user_group_ids(user_id)
            return groups
        except VkApiError:
            subs = self.get_user_subscription_ids(user_id)
            return subs

    def get_groups_extended_info(self, group_ids):
        """
        use info from wall
        """

        def __extend_group_info(group):
            group_id = group['id']
            try:
                group['wall'] = self.get_group_wall(group_id)
            except VkApiError as e:
                group['errors'] = [e]

            return group

        groups_info = self.get_groups_info(group_ids)
        groups_info = map(lambda g: __extend_group_info(g), groups_info)
        return list(groups_info)

    @staticmethod
    def __chunk_data(data, chunk_size):
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]

    def get_groups_info(self, group_ids):
        group_ids_chunks = list(self.__chunk_data(group_ids, 100))
        res = []
        for chunk in group_ids_chunks:
            group_ids_str = ','.join(map(str, chunk))
            fields = 'activity,age_limits,description,status'
            response = self.__send(vkApi.get_groups_by_id, access_token=self.__access_token, group_ids=group_ids_str,
                                   fields=fields)
            res.extend(response.response)
        return res

    def get_friends(self, user_id):
        """
        https://vk.com/dev/friends.get
        """
        response = self.__send(vkApi.get_friends, access_token=self.__access_token, user_id=user_id, count=10000)
        return response['items']

    def get_group_wall(self, group_id: int):
        """
        https://vk.com/dev/wall.get
        """
        response = self.__send(vkApi.get_wall, access_token=self.__access_token, owner_id=-group_id, count=100)
        return response['items']


class TimeoutExpiredError(Exception):
    def __init__(self, timeout):
        super().__init__(f'the timeout ({timeout}) has expired')


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
