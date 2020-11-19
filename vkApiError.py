class VkApiError(Exception):
    def __init__(self, error_response):
        self.error_code = error_response['error_code']
        self.error_msg = error_response['error_msg']
        self.request_params = error_response['request_params']
        message = f'{str(error_response)}\n see https://vk.com/dev/errors'
        super().__init__(message)
