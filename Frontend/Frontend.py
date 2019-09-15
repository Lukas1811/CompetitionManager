from flask import Flask

from Backend.Competition import Competition

class Frontend:
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.app = Flask(self.app_name)

