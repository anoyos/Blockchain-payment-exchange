from flask import Flask
from flask_compress import Compress


class Application(Flask):

    def __init__(self, app_name: str, flask_conf: dict):
        super(Application, self).__init__(app_name)

        self.config.update(flask_conf)
        self.after_request(after_request)
        self._port = flask_conf['http_port']

        Compress(self)

    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        super().run(host, self._port, debug, load_dotenv, **options)


def after_request(response):
    response.headers[
        "Cache-Control"
    ] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"

    return response
