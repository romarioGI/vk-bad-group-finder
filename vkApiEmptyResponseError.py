class VkApiEmptyResponseError(Exception):
    def __init__(self):
        super().__init__('response is empty')
