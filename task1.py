class Task1:
    @classmethod
    def solve(cls, content_analyzers: list, users_id: list) -> dict:
        return dict(map(lambda user_id: (user_id, cls.__try_solve(content_analyzers, user_id)), users_id))

    @classmethod
    def __try_solve(cls, content_analyzers: list, user_id):
        try:
            return cls.__solve(content_analyzers, user_id)
        except Exception as e:
            return {'error': str(e)}

    @classmethod
    def __solve(cls, content_analyzers: list, user_id) -> dict:
        groups = cls.__get_groups_info(user_id)
        return dict(map(
            lambda g: (g['id'], cls.__analyze_group(content_analyzers, g)),
            groups
        ))

# TODO
    @classmethod
    def __get_groups_info(cls, user_id) -> list:
        pass

    @classmethod
    def __analyze_group(cls, content_analyzers: list, group_info: dict) -> dict:
        name = group_info['name']
        tags = list(map(
            lambda c_a: c_a.tag,
            filter(
                lambda c_a: c_a.check(group_info),
                content_analyzers
            )
        ))
        return {'name': name, 'tags': tags}
