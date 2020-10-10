# constants, import from appconfig
baseUrl = "https://api.vk.com/method"


def get_request_string(methodName: str, params: dict) -> str:
    paramsString = "&".join(map(lambda p: p[0] + "=" + p[1], params.items()))
    return baseUrl + "/" + methodName + "?" + paramsString
