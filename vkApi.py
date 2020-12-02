import requests

API_URL_BASE = 'https://api.vk.com/method'
API_VERSION = '5.124'


def get_api_request(method_name: str, access_token: str, params: dict) -> requests.Response:
    params['access_token'] = access_token
    params['v'] = API_VERSION
    url = f'{API_URL_BASE}/{method_name}'
    return requests.get(url, params=params)


def get_utils_resolve_screen_name(access_token: str, screen_name: str):
    """
    https://vk.com/dev/utils.resolveScreenName
    """
    params = {'screen_name': screen_name}
    method_name = 'utils.resolveScreenName'
    return get_api_request(method_name, access_token, params)


def get_user_subscriptions(access_token: str, user_id=None, extended=None, offset=None, count=None, fields=None):
    """
    https://vk.com/dev/users.getSubscriptions
    """
    params = {
        'user_id': user_id,
        'extended': extended,
        'offset': offset,
        'count': count,
        'fields': fields
    }
    method_name = 'users.getSubscriptions'
    return get_api_request(method_name, access_token, params)


def get_user_groups(access_token: str, user_id=None, extended=None, filter=None, fields=None, offset=None, count=None):
    """
    https://vk.com/dev/groups.get
    """
    params = {
        'user_id': user_id,
        'extended': extended,
        'filter': filter,
        'fields': fields,
        'offset': offset,
        'count': count
    }
    method_name = 'groups.get'
    return get_api_request(method_name, access_token, params)


def get_groups_by_id(access_token: str, group_ids=None, group_id=None, fields=None):
    """
    https://vk.com/dev/groups.getById
    """
    params = {
        'group_ids': group_ids,
        'group_id': group_id,
        'fields': fields
    }
    method_name = 'groups.getById'
    return get_api_request(method_name, access_token, params)


def get_friends(access_token: str, user_id=None, order=None, list_id=None, count=None, offset=None, fields=None,
                name_case=None, ref=None):
    """
    https://vk.com/dev/friends.get
    """
    params = {
        'user_id': user_id,
        'order': order,
        'list_id': list_id,
        'count': count,
        'offset': offset,
        'fields': fields,
        'name_case': name_case,
        'ref': ref
    }
    method_name = 'friends.get'
    return get_api_request(method_name, access_token, params)


def __params_to_str(params: dict) -> str:
    params = filter(
        lambda p: p[1] is not None,
        params.items()
    )
    return '&'.join(map(
        lambda p: f'{p[0]}={p[1]}',
        params
    ))


def build_get_access_code_request_str(client_id, redirect_uri: str, scope) -> str:
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope,
        'revoke': 1,
        'response_type': 'code',
        'v': API_VERSION
    }
    method = 'authorize'
    params_str = __params_to_str(params)
    return f'https://oauth.vk.com/{method}?{params_str}'


def build_get_access_token_request_str(client_id, client_secret, redirect_uri: str, code) -> str:
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code,
        'v': API_VERSION
    }
    method = 'access_token'
    params_str = __params_to_str(params)
    return f'https://oauth.vk.com/{method}?{params_str}'
