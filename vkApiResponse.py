from requests import Response

from vkApiError import VkApiError


# также бывают execute_errors, которые возникают при исполнении кода на стороне VK
# при необходисмости их можно обрабатывать
class VkApiResponse:
    def __init__(self, api_response: Response):
        response = api_response.json()
        if 'error' in response:
            raise VkApiError(response['error'])
        elif 'response' in response:
            self.__response = response['response']
        else:
            raise Exception('wrong response format')
        if isinstance(self.response, dict):
            self.__is_object = True
        else:
            self.__is_object = False

    @property
    def is_empty(self):
        response = self.response
        return (isinstance(response, list) or isinstance(response, dict)) and len(response) == 0

    @property
    def response(self):
        return self.__response

    def __getitem__(self, attribute: str):
        if not self.__is_object:
            raise Exception('response is not object (dict) and does not have the any attributes')
        if attribute in self.response:
            return self.response[attribute]
        raise AttributeError(f'response does not have the {attribute} attribute')
