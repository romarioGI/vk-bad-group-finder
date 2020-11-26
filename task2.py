from task1 import Task1
from vkApiWrapper import VkApiWrapper


class Task2:
    def __init__(self, access_token: str, content_analyzers: list, vkApiWrapper: VkApiWrapper):
        self.__access_token = access_token
        self.__content_analyzers = content_analyzers
        self.__vkApiWrapper = vkApiWrapper

    def solve(self, users_id: list, show_untagged: bool = False, ignore_private_accounts: bool = True) -> dict:
        return dict(map(
            lambda user_id: (user_id, self.__try_solve(user_id, show_untagged, ignore_private_accounts)),
            users_id
        ))

    def __try_solve(self, user_id, show_untagged: bool, ignore_private_accounts: bool):
        try:
            return self.__solve(user_id, show_untagged, ignore_private_accounts)
        except Exception as e:
            return {'error': e}

    def __solve(self, user_id, show_untagged: bool, ignore_private_accounts: bool) -> dict:
        friends = self.__vkApiWrapper.get_friends(self.__access_token, user_id)
        task1 = Task1(self.__access_token, self.__content_analyzers, self.__vkApiWrapper)
        return task1.solve(friends, show_untagged, ignore_private_accounts)
