from task1 import Task1
from vkApiWrapper import VkApiWrapper, VkApiError


class Task2:
    def __init__(self, content_analyzers: list, vkApiWrapper: VkApiWrapper):
        self.__content_analyzers = content_analyzers
        self.__vkApiWrapper = vkApiWrapper

    def solve(self, users_id: list, show_untagged_group: bool = False, ignore_private_accounts: bool = True,
              use_extended_group_info: bool = True, ignore_empty_friends: bool = True) -> dict:
        return dict(map(
            lambda user_id: (
                user_id,
                self.__try_solve(user_id, show_untagged_group, ignore_private_accounts, use_extended_group_info,
                                 ignore_empty_friends)),
            users_id
        ))

    def __try_solve(self, user_id, show_untagged: bool, ignore_private_accounts: bool, use_extended_group_info: bool,
                    ignore_empty_friends: bool):
        try:
            return {'friends': self.__solve(user_id, show_untagged, ignore_private_accounts, use_extended_group_info,
                                            ignore_empty_friends)}
        except VkApiError as e:
            return {'error': e}

    def __solve(self, user_id, show_untagged: bool, ignore_private_accounts: bool, use_extended_group_info: bool,
                ignore_empty_friends: bool) -> dict:
        friends = self.__vkApiWrapper.get_friends(user_id)
        task1 = Task1(self.__content_analyzers, self.__vkApiWrapper)
        res = task1.solve(friends, show_untagged, ignore_private_accounts, use_extended_group_info)
        if ignore_empty_friends:
            res = filter(lambda p: not (('groups' in p[1]) and (len(p[1]['groups']) == 0)), res.items())
        return dict(res)
