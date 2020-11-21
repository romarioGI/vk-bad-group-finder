from task1 import Task1
from vkApi import VkApi


class Task2:
    def __init__(self, access_token: str, content_analyzers: list):
        self.__access_token = access_token
        self.__content_analyzers = content_analyzers

    def solve(self, users_id: list) -> dict:
        return dict(map(
            lambda user_id: (user_id, self.__try_solve(user_id)),
            users_id
        ))

    def __try_solve(self, user_id):
        try:
            return self.__solve(user_id)
        except Exception as e:
            return {'error': e}

    def __solve(self, user_id) -> dict:
        friends = self.__get_friends_ids(user_id)
        task1 = Task1(self.__access_token, self.__content_analyzers)
        return dict(map(
            lambda f_id: (f_id, task1.solve(f_id)),
            friends
        ))

    def __get_friends_ids(self, user_id) -> list:
        friends = VkApi.get_friends(self.__access_token, user_id)['items']
        return list(map(lambda f: f['id'], friends))
