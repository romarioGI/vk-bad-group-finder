from flask import Flask, request
import logging


class AuthRequestRedirectServer:
    def __init__(self, host, port, callback):
        self.host = host
        self.port = port
        self.__app = Flask(__name__)
        self.__callback = callback
        self.__is_alive = True
        log = logging.getLogger('werkzeug')
        log.disabled = True
        self.__app.logger.disabled = True

        @self.__app.route('/')
        def index():
            return 'running'

        @self.__app.route('/vk_auth')
        def vk_auth():
            args = dict(request.args)
            try:
                if 'code' in args:
                    page = f'<h1>ACCEPTED</h1><p>close browser, return to app</p>'
                else:
                    page = f'<h1>troubles</h1><p>{str(args)}</p><p>close browser, return to app</p>'
                return page
            finally:
                if self.__is_alive:
                    self.__is_alive = False
                    self.__callback(args)

    def run(self):
        self.__app.run(host=self.host, port=self.port, debug=False, use_reloader=False)
