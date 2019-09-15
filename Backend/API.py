from flask import request
import os

from Backend.Competition import Competition
from Backend.logger import Logger as log

class API:
    def __init__(self, app, db_folder: str):
        self.app = app
        self.app.config['UPLOAD_FOLDER'] = db_folder

        self.db_folder = db_folder

        self.competitions = {}

        self.url_endpoints = [
            ["/competition/<string:competition_name>/new", "new_competition", self.new_competition, ["GET"]],
            ["/competition/<string:competition_name>/load", "load_competition", self.load_competition, ["GET"]],
            ["/competition/<string:competition_name>/save", "save_competition", self.save_competition, ["GET"]],
            ["/competition/<string:competition_name>/import_archers", "import_archers", self.import_archers, ["GET"]],
            ["/competition/<string:competition_name>/archers", "get_archers", self.get_archers, ["GET"]],
            ["/competition/<string:competition_name>/add_archer", "add_archer", self.add_archer, ["GET"]],
            ["/competition/<string:competition_name>/add_bow_type", "add_bow_type", self.add_bow_type, ["GET"]],
            ["/competition/<string:competition_name>/add_class", "add_class", self.add_class, ["GET"]]
        ]

        for endpoint in self.url_endpoints:
            self.app.add_url_rule(endpoint[0], endpoint[1], endpoint[2])

        log.info("Initialized API")

    def new_competition(self, competition_name: str):
        competition = Competition(competition_name, self.db_folder + competition_name)
        competition.save()

        log.info("Created competition {0}".format(competition_name))

        self.competitions.update({competition_name: competition})

        return {
            "status": "SUCCESS",
            "competition_name": competition_name,
            "new": True
        }

    def load_competition(self, competition_name: str):
        if competition_name not in self.competitions:
            try:
                competition = Competition.load_competition(self.db_folder + competition_name)
                self.competitions.update({competition_name: competition})

                return {
                    "status": "SUCCESS",
                    "competition_name": competition_name,
                    "new": False
                }
            except OSError:
                log.error("Could not find config for competition {0}".format(competition_name))

                return {
                    "status": "ERROR",
                    "error_message": "ALREADY_LOADED",
                    "competition_name": competition_name,
                    "new": False
                }

            except Exception as exc:
                log.info("Could not find config for competition {0} \n Exception: {1}".format(competition_name, exc))

                return {
                    "status": "ERROR",
                    "error_message": "CONFIG_LOADING_ERROR",
                    "competition_name": competition_name,
                    "new": False
                }

        elif competition_name in self.competitions:
            return {
                "status": "ERROR",
                "error_message": "ALREADY_LOADED"
                }

    def save_competition(self, competition_name: str):
        if competition_name not in self.competitions:
            log.warn("Competition not loaded, can not save competition!")

            return {
                "status": "ERROR",
                "error_message": "COMPETITION_NOT_LOADED"
            }

        else:
            self.competitions[competition_name].save()

        return {
            "status": "SUCCESS"
        }

    def import_archers(self, competition_name: str):
        if competition_name not in self.competitions:
            log.warn("Competition not loaded, can not import archers!")
            return

        if request.method == "POST":
            if "file" not in request.files:
                log.warn("No file in request")
            else:
                file = request.files["file"]
                path = self.app.config["UPLOAD_FOLDER"]

                file.save(os.path.join(path, competition_name + "_archers"))

                self.competitions[competition_name].import_archers(path + "/{0}_archers".format(competition_name))

                return {
                    "status": "SUCCESS",
                    "new_archers": len(self.competitions[competition_name].archers)
                    }

    def get_archers(self, competition_name: str):
        if request.method == "GET":
            return {
                "status": "SUCCESS",
                "archers": self.competitions[competition_name].archers
                }

    def add_archer(self, competition_name: str):
        if competition_name in self.competitions:
            request_data = request.get_json()

            if request_data:
                competition = self.competitions[competition_name]

                name = request_data["name"]
                bow_type = request_data["bow"]
                archer_class = request_data["class"]

                competition.add_archer(name, bow_type, archer_class)

                log.info("Added new archer (name: {0}, bow: {1}, class: {2}".format(name, bow_type, archer_class))

                return {
                    "status": "SUCCESS"
                }
        else:
            log.error("No competition with name {0} loaded".format(competition_name))

            return {
                "status": "ERROR",
                "error_message": "UNKNOWN_COMPETITION"
            }

    def add_bow_type(self, competition_name: str):
        if competition_name in self.competitions:
            request_data = request.get_json()

            if request_data:
                competition = self.competitions[competition_name]

                bow_type = request_data["bow"]

                competition.add_bow(bow_type)

                return {
                    "status": "SUCCESS"
                }

    def add_class(self, competition_name: str):
        if competition_name in self.competitions:
            request_data = request.get_json()

            if request_data:
                competition = self.competitions[competition_name]

                archer_class = request_data["class"]

                competition.add_class(archer_class)

                return {
                    "status": "SUCCESS"
                }

