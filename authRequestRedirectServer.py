from flask import Flask, request
from threading import Lock


class AuthRequestRedirectServer:
    def __init__(self, host, port, lock: Lock):
        self.host = host
        self.port = port
        self.__app = Flask(__name__)
        self.__app.debug = False
        self.__app.use_reloader = False
        self.__lock = lock
        self.output = None

        @self.__app.route('/')
        def index():
            return 'running'

        @self.__app.route('/vk_auth')
        def vk_auth():
            args = dict(request.args)
            try:
                if 'code' in args:
                    return f'<h1>ACCEPTED</h1><p>close browser, return to app</p>'
                else:
                    return f'<h1>troubles</h1><p>{str(args)}</p><p>close browser, return to app</p>'
            finally:
                self.output = args
                self.__lock.release()

    def run(self):
        self.__app.run(host=self.host, port=self.port, debug=False, use_reloader=False)
