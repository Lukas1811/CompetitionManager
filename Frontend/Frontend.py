from os.path import abspath
from flask import send_from_directory, render_template

from Backend.Competition import Competition
from Backend.logger import Logger as log

class Frontend:
    CSS_DIR = "./Frontend/css/"
    JS_DIR = "./Frontend/js/"
    HTML_DIR = "./Frontend/html/"

    def __init__(self, app: object):
        self.app = app

        self.url_endpoints = [
            ["/static/js/<string:file>/", "static_js", self.static_js, ["GET"]],
            ["/static/css/<string:file>/", "static_css", self.static_css, ["GET"]],
            ["/", "index_html", self.index, ["GET"]],
            ["/scoring/", "scoring_html", self.scoring, ["GET"]],
            ["/new_competition/", "new_competition_html", self.scoring, ["GET"]],
            ["/edit_competition/", "edit_competition_html", self.edit, ["GET"]],
        ]

        for endpoint in self.url_endpoints:
            self.app.add_url_rule(endpoint[0], endpoint[1], endpoint[2])

        log.info("Initialized Frontend")

    def static_js(self, file: str):
        return send_from_directory(Frontend.JS_DIR, file)

    def static_css(self, file: str):
        return send_from_directory(Frontend.CSS_DIR, file)

    def index(self):
        return render_template("index.html")

    def scoring(self):
        return render_template("scoring.html")

    def new_competition(self):
        return render_template("new.html")

    def edit(self):
        return render_template("settings.html")
