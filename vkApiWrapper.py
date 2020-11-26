import random
import webbrowser
from collections import deque
from datetime import datetime
from threading import Thread, Lock
from time import sleep

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


class VkApiRequestSender:
    __TOO_MANY_REQUESTS_ERROR_CODE = 6

    def __init__(self, attempts_number: int, request_per_second_limit: int):
        if attempts_number < 1:
            raise Exception('attempts_number should be not less then 1')
        self.attempts_number = attempts_number
        if request_per_second_limit < 1:
            raise Exception('request_per_second_limit should be not less then 1')
        self.request_per_second_limit = request_per_second_limit
        self.__request_between_time = 1.0 / self.request_per_second_limit
        self.__request_queue = deque()
        self.__queue_lock = Lock()

    def __calc_sleep_time(self):
        self.__queue_lock.acquire()
        try:
            now = datetime.now()
            self.__request_queue.append(now)
            while True:
                front = self.__request_queue[0]
                seconds = (now - front).total_seconds()
                if seconds > 1:
                    self.__request_queue.popleft()
                else:
                    break
            if len(self.__request_queue) <= self.request_per_second_limit:
                seconds = 0
            return seconds
        finally:
            self.__queue_lock.release()

    def send(self, f):
        fails_count = 0
        last_e = None
        sleep_time = self.__calc_sleep_time()
        sleep(sleep_time)
        while fails_count < self.attempts_number:
            try:
                return f()
            except VkApiError as e:
                if e.error_code == self.__TOO_MANY_REQUESTS_ERROR_CODE:
                    last_e = e
                    fails_count += 1
                    sleep(self.__request_between_time)
                else:
                    raise e

        raise last_e


class VkApiWrapper:
    def __init__(self, request_attempts_number: int = 1, request_per_second_limit: int = 3):
        self.__sender = VkApiRequestSender(request_attempts_number, request_per_second_limit)

    def __send(self, api_request_func, **params) -> VkApiResponse:
        def f():
            response = api_request_func(**params)
            return VkApiResponse(response)

        return self.__sender.send(f)

    def get_user_id(self, access_token: str, screen_name: str) -> int:
        """
        https://vk.com/dev/utils.resolveScreenName
        """
        response = self.__send(vkApi.get_utils_resolve_screen_name, access_token=access_token, screen_name=screen_name)
        if response.is_empty:
            raise UserNotFound(screen_name)
        object_type = response['type']
        if object_type != 'user':
            raise UserNotFound(screen_name)
        object_id = response['object_id']
        return object_id

    @staticmethod
    def __get_fields():
        fields = ['age_limits', 'description', 'main_album_id', 'status']
        return ','.join(fields)

    def get_user_subscription_ids(self, access_token: str, user_id) -> list:
        """
        https://vk.com/dev/users.getSubscriptions
        """
        response = self.__send(vkApi.get_user_subscriptions, access_token=access_token, user_id=user_id, extended=0)
        res = response['groups']['items']
        return res

    def get_user_group_ids(self, access_token: str, user_id) -> list:
        """
        https://vk.com/dev/groups.get
        """
        res = []
        while True:
            response = self.__send(vkApi.get_user_groups, access_token=access_token, user_id=user_id, extended=0,
                                   offset=len(res), count=1000)
            cur = response['items']
            res.extend(cur)
            if len(res) >= response['count']:
                break
        return res

    def try_get_user_group_ids(self, access_token: str, user_id) -> list:
        try:
            groups = self.get_user_group_ids(access_token, user_id)
            return groups
        except VkApiError:
            subs = self.get_user_subscription_ids(access_token, user_id)
            return subs

    def get_friends(self, access_token: str, user_id):
        response = self.__send(vkApi.get_friends, access_token=access_token, user_id=user_id, count=10000)
        return response['items']

    @staticmethod
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
