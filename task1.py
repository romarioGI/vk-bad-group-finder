from vkApi import VkApi


class Task1:
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
        groups = self.__get_groups_info(user_id)
        return dict(map(
            lambda g: (g['id'], self.__analyze_group(g)),
            groups
        ))

    # TODO
    def __get_groups_info(self, user_id) -> list:
        return VkApi.get_user_groups(user_id, self.__access_token)['items']

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
