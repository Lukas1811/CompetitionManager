from os.path import abspath
from flask import Flask, send_from_directory

from Backend.Competition import Competition
from Backend.logger import Logger as log

class Frontend:
    def __init__(self, app: object):
        self.app = app

        self.html_dir = abspath("./Frontend/html")
        self.css_dir = abspath("./Frontend/css")
        self.js_dir = abspath("./Frontend/js")

        print(self.html_dir)

        self.url_endpoints = [
            ["/static/js/<string:file>/", "static_js", self.static_js, ["GET"]],
            ["/static/css/<string:file>/", "static_css", self.static_css, ["GET"]],
            ["/<string:file>/", "static_html", self.static_html, ["GET"]],
            ["/<string:file>/", "static_html", self.static_html, ["GET"]],
            ["/", "index_html", self.static_html, ["GET"]],
        ]

        for endpoint in self.url_endpoints:
            self.app.add_url_rule(endpoint[0], endpoint[1], endpoint[2])

        log.info("Initialized Frontend")

    def static_js(self, file: str):
        return send_from_directory(self.js_dir, file)

    def static_css(self, file: str):
        return send_from_directory(self.css_dir, file)

    def static_html(self, file="index.html"):
        return send_from_directory(self.html_dir, file)

