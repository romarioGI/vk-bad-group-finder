from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class Handler(BaseHTTPRequestHandler):
    def __init__(self, callback, *args):
        self.__callback = callback
        super().__init__(*args)

    def __send_ok(self, body: str):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    @staticmethod
    def __get_args(url):
        args = parse_qs(url.query)
        res = dict()
        for key, val in args.items():
            res[key] = val[0]
        return res

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/":
            self.__send_ok('running')
        elif url.path == '/vk_auth':
            args = self.__get_args(url)
            if 'code' in args:
                body = f'<h1>ACCEPTED</h1><p>close browser, return to app</p>'
            else:
                body = f'<h1>troubles</h1><p>{str(args)}</p><p>close browser, return to app</p>'
            self.__send_ok(body)
            self.__callback(args)
        else:
            self.send_error(404)


class AuthRequestRedirectServer:
    def __init__(self, host: str, port: int, callback):
        server_address = (host, port)
        self.__httpd = HTTPServer(server_address, lambda *args: Handler(callback, *args))

    def run(self):
        self.__httpd.serve_forever()

    def stop(self):
        self.__httpd.shutdown()
