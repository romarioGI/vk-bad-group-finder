from collections import deque
from datetime import datetime
from threading import Lock
from time import sleep

from vkApiError import VkApiError
from vkApiErrorCodes import TOO_MANY_REQUESTS_ERROR_CODE


class VkApiRequestSender:
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
                if seconds > 1.0:
                    self.__request_queue.popleft()
                else:
                    break
            if len(self.__request_queue) <= self.request_per_second_limit:
                seconds = 0
            return seconds
        finally:
            self.__request_queue.pop()
            self.__queue_lock.release()

    def __add_sending(self):
        self.__queue_lock.acquire()
        try:
            now = datetime.now()
            self.__request_queue.append(now)
        finally:
            self.__queue_lock.release()

    def send(self, f):
        fails_count = 0
        last_e = None
        sleep_time = self.__calc_sleep_time()
        sleep(sleep_time)
        while fails_count < self.attempts_number:
            try:
                res = f()
                self.__add_sending()
                return res
            except VkApiError as e:
                if e.error_code == TOO_MANY_REQUESTS_ERROR_CODE:
                    last_e = e
                    fails_count += 1
                    sleep(self.__request_between_time)
                else:
                    raise e

        raise last_e
