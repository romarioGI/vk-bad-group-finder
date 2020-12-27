class VkApiError(Exception):
    def __init__(self, error_response):
        self.error_code = error_response['error_code']
        self.error_msg = f'{str(error_response)}\n see https://vk.com/dev/errors'
        super().__init__(self.error_msg)
