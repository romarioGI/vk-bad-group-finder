from vkApiErrorCodes import PRIVATE_PROFILE_ERROR_CODE
from vkApiWrapper import VkApiWrapper, VkApiError


class Task1:
    def __init__(self, content_analyzers: list, vkApiWrapper: VkApiWrapper):
        self.__content_analyzers = content_analyzers
        self.__vkApiWrapper = vkApiWrapper

    def solve(self, users_id: list, show_untagged_group: bool = False, ignore_private_accounts: bool = True,
              use_extended_group_info: bool = True) -> dict:
        res = map(
            lambda user_id: (user_id, self.__try_solve(user_id, show_untagged_group, use_extended_group_info)),
            users_id
        )
        if ignore_private_accounts:
            res = filter(
                lambda i: not ('error' in i[1] and isinstance(i[1]['error'], VkApiError)
                               and i[1]['error'].error_code == PRIVATE_PROFILE_ERROR_CODE),
                res
            )
        return dict(res)

    def __try_solve(self, user_id, show_untagged: bool, use_extended_group_info: bool) -> dict:
        try:
            return {'groups': self.__solve(user_id, show_untagged, use_extended_group_info)}
        except VkApiError as e:
            return {'error': e}

    def __solve(self, user_id, show_untagged: bool, use_extended_group_info: bool) -> dict:
        group_ids = self.__vkApiWrapper.try_get_user_group_ids(user_id)
        if use_extended_group_info:
            groups = self.__vkApiWrapper.get_groups_extended_info(group_ids)
        else:
            groups = self.__vkApiWrapper.get_groups_info(group_ids)
        res = map(
            lambda g: (g['id'], self.__analyze_group(g)),
            groups
        )
        if not show_untagged:
            res = filter(
                lambda g: not (('tags' in g[1]) and (len(g[1]['tags'])) == 0),
                res
            )

        return dict(res)

    def __analyze_group(self, group: dict) -> dict:
        name = group['name']
        tags = []
        for c_a in self.__content_analyzers:
            tag = c_a(group)
            if tag is not None:
                tags.append(tag)
        return {'name': name, 'tags': tags}
