class TimeoutExpiredError(Exception):
    def __init__(self, timeout):
        super().__init__(f'the timeout ({timeout}) has expired')
