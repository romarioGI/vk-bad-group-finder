import vkApiExtensionMethods
from vkApiRequestSender import VkApiRequestSender


class Task1:
    __PRIVATE_PROFILE_ERROR_CODE = 30

    def __init__(self, access_token: str, content_analyzers: list, sender: VkApiRequestSender):
        self.__access_token = access_token
        self.__content_analyzers = content_analyzers
        self.__sender = sender

    def solve(self, users_id: list, show_untagged: bool = False, ignore_private_accounts: bool = True) -> dict:
        res = map(
            lambda user_id: (user_id, self.__try_solve(user_id, show_untagged)),
            users_id
        )
        if ignore_private_accounts:
            res = filter(
                lambda i: not (isinstance(i[1], vkApiExtensionMethods.VkApiError)
                               and i[1].error_code == self.__PRIVATE_PROFILE_ERROR_CODE),
                res
            )
        return dict(res)

    def __try_solve(self, user_id, show_untagged: bool):
        try:
            return self.__solve(user_id, show_untagged)
        except Exception as e:
            return {'error': e}

    def __solve(self, user_id, show_untagged: bool) -> dict:
        def f():
            return vkApiExtensionMethods.try_get_user_groups(self.__access_token, user_id)

        groups = self.__sender.send(f)
        res = map(
            lambda g: (g['id'], self.__analyze_group(g)),
            groups
        )
        if not show_untagged:
            res = filter(
                lambda g: 'tags' in g[1] and len(g[1]['tags']) != 0,
                res
            )

        return dict(res)

    def __analyze_group(self, group: dict) -> dict:
        name = group['name']
        tags = list(map(
            lambda c_a: c_a.tag,
            filter(
                lambda c_a: c_a.check(group),
                self.__content_analyzers
            )
        ))
        return {'name': name, 'tags': tags}
