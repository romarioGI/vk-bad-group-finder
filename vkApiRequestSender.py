from time import sleep
from vkApiExtensionMethods import VkApiError


class VkApiRequestSender:
    __TOO_MANY_REQUESTS_ERROR_CODE = 6

    def __init__(self, attempts_number: int, request_per_second_limit: int = 3):
        if attempts_number < 1:
            raise Exception('attempts_number should be not less then 1')
        self.attempts_number = attempts_number
        if request_per_second_limit < 1:
            raise Exception('request_per_second_limit should be not less then 1')
        self.__request_between_time = 1.0 / request_per_second_limit

    def send(self, f):
        fails_count = 0
        last_e = None
        while fails_count < self.attempts_number:
            try:
                return f()
            except VkApiError as e:
                if e.error_code == self.__TOO_MANY_REQUESTS_ERROR_CODE:
                    last_e = e
                    fails_count += 1
                    sleep(fails_count)
                else:
                    raise e
            finally:
                sleep(self.__request_between_time)

        raise last_e
