from flask import request, jsonify
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
            ["/competition/existing", "existing_competitions", API.existing_competitions, ["GET"]],
            ["/competition/new", "new_competition", self.new_competition, ["POST"]],
            ["/competition/<string:competition_name>/update", "update_competition", self.update_competition_info, ["POST"]],
            ["/competition/<string:competition_name>/data", "get_competition_data", self.get_competition_data, ["GET"]],
            ["/competition/<string:competition_name>/load", "load_competition", self.load_competition, ["GET"]],
            ["/competition/<string:competition_name>/save", "save_competition", self.save_competition, ["GET"]],
            ["/competition/<string:competition_name>/import_archers", "import_archers", self.import_archers, ["GET"]],
            ["/competition/<string:competition_name>/archers", "get_archers", self.get_archers, ["GET"]],
            ["/competition/<string:competition_name>/sorted_archers", "get_sorted_archers", self.get_sorted_archers, ["GET"]],
            ["/competition/<string:competition_name>/add_archer", "add_archer", self.add_archer, ["POST"]],
            ["/competition/<string:competition_name>/import_archers", "import_archers", self.import_archers, ["POST"]],
            ["/competition/<string:competition_name>/remove_archer", "remove_archer", self.remove_archer, ["POST"]],
            ["/competition/<string:competition_name>/add_bow", "add_bow_type", self.add_bow_type, ["POST"]],
            ["/competition/<string:competition_name>/remove_bow", "remove_bow_type", self.remove_bow_type, ["POST"]],
            ["/competition/<string:competition_name>/add_class", "add_class", self.add_class, ["POST"]],
            ["/competition/<string:competition_name>/remove_class", "remove_class", self.remove_class, ["POST"]],
            ["/competition/<string:competition_name>/update_score", "update_score", self.update_score, ["POST"]],
        ]

        for endpoint in self.url_endpoints:
            self.app.add_url_rule(endpoint[0], endpoint[1], endpoint[2], methods=endpoint[3])

        log.info("Initialized API")

    def new_competition(self):
        try:
            competition = Competition(request.json["name"], self.db_folder + request.json["name"])
            competition.set_date(request.json["date"])
            competition.set_description(request.json["description"])
            competition.save()

            log.info("Created competition {0}".format(request.json["name"]))

            self.competitions.update({request.json["name"]: competition})

            return jsonify({
                "status": "SUCCESS"
            })

        except KeyError:
            log.warn("Received invalid request for creating competition")

        return jsonify({
            "status": "ERROR"
        })


    def update_competition_info(self, competition_name: str):
        if competition_name in self.competitions:
            try:
                self.competitions[competition_name].set_name(request.json["name"])
                self.competitions[competition_name].set_date(request.json["date"])
                self.competitions[competition_name].set_description(request.json["description"])
                return jsonify({
                    "status": "SUCCESS"
                })

            except KeyError:
                log.warn("Received invalid request for updating competition {0}".format(competition_name))
        else:
            log.warn("Competition {0} not loaded couldn't update".format(competition_name))

    def get_competition_data(self, competition_name: str):
        if competition_name in self.competitions:
            return jsonify({
                "description": self.competitions[competition_name].description,
                "date": self.competitions[competition_name].date,
                "bows": self.competitions[competition_name].bow_types,
                "classes": self.competitions[competition_name].archer_classes
            })

        else:
            log.warn("Competition {0} not loaded couldn't update".format(competition_name))


    def load_competition(self, competition_name: str):
        if competition_name not in self.competitions:
            try:
                competition = Competition.load_competition(self.db_folder + competition_name)
                self.competitions.update({competition_name: competition})

                return jsonify({
                    "status": "SUCCESS",
                    "competition_name": competition_name,
                    "new": False
                })
            except OSError:
                log.error("Could not find config for competition {0}".format(competition_name))

                return jsonify({
                    "status": "ERROR",
                    "error_message": "ALREADY_LOADED",
                    "competition_name": competition_name,
                    "new": False
                })

            except Exception as exc:
                log.info("Could not find config for competition {0} \n Exception: {1}".format(competition_name, exc))

                return jsonify({
                    "status": "ERROR",
                    "error_message": "CONFIG_LOADING_ERROR",
                    "competition_name": competition_name,
                    "new": False
                })

        elif competition_name in self.competitions:
            return jsonify({
                "status": "ERROR",
                "error_message": "ALREADY_LOADED"
                })

    def save_competition(self, competition_name: str):
        if competition_name not in self.competitions:
            log.warn("Competition not loaded, can not save competition!")

            return jsonify({
                "status": "ERROR",
                "error_message": "COMPETITION_NOT_LOADED"
            })

        else:
            self.competitions[competition_name].save()

        return jsonify({
            "status": "SUCCESS"
        })

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

                return jsonify({
                    "status": "SUCCESS",
                    "new_archers": len(self.competitions[competition_name].archers)
                    })

    def get_archers(self, competition_name: str):
        if request.method == "GET":
            if competition_name in self.competitions:
                archers_list = []
                for archer in self.competitions[competition_name].archers:
                    archers_list.append(archer.to_dict())

                return jsonify({
                    "status": "SUCCESS",
                    "archers": archers_list
                    })

    def get_sorted_archers(self, competition_name: str):
        if request.method == "GET":
            if competition_name in self.competitions:
                print("test")
                return jsonify(self.competitions[competition_name].to_sorted_dict())

    def add_archer(self, competition_name: str):
        if competition_name in self.competitions:
            request_data = request.get_json()

            if request_data:
                competition = self.competitions[competition_name]

                name = request_data["name"]
                bow_type = request_data["bow"]
                archer_class = request_data["class"]
                archer_club = request_data["club"]

                competition.add_archer(name, bow_type, archer_class, archer_club)

                log.info("Added new archer (name: {0}, bow: {1}, class: {2}".format(name, bow_type, archer_class))

                return jsonify({
                    "status": "SUCCESS"
                })
        else:
            log.error("No competition with name {0} loaded".format(competition_name))

            return jsonify({
                "status": "ERROR",
                "error_message": "UNKNOWN_COMPETITION"
            })

    def remove_archer(self, competition_name: str):
        if competition_name in self.competitions:
            request_data = request.get_json()

            for archer in self.competitions[competition_name].archers:
                if archer.name == request_data["archer"]:
                    self.competitions[competition_name].remove_archer(archer)

            return jsonify({
                "status": "SUCCESS"
            })

    def update_score(self, competition_name: str):
        if request.method == "POST":
            if competition_name in self.competitions:
                request_data = request.get_json()["data"]
                print(request_data)

                self.competitions[competition_name].update_score(request_data["name"],
                                                                 request_data["club"],
                                                                 int(request_data["round_index"]),
                                                                 int(request_data["round_score"]),)

                return jsonify(self.competitions[competition_name].to_sorted_dict())


    def add_bow_type(self, competition_name: str):
        if competition_name in self.competitions:
            request_data = request.get_json()

            if request_data:
                competition = self.competitions[competition_name]

                bow_type = request_data["bow"]

                competition.add_bow(bow_type)

                return jsonify({
                    "status": "SUCCESS"
                })

    def remove_bow_type(self, competition_name: str):
        if competition_name in self.competitions:
            request_data = request.get_json()

            if request_data:
                competition = self.competitions[competition_name]

                bow_type = request_data["bow"]

                competition.remove_bow(bow_type)

                return jsonify({
                    "status": "SUCCESS"
                })

    def add_class(self, competition_name: str):
        if competition_name in self.competitions:
            request_data = request.get_json()

            if request_data:
                competition = self.competitions[competition_name]

                archer_class = request_data["class"]

                competition.add_class(archer_class)

                return jsonify({
                    "status": "SUCCESS"
                })

    def remove_class(self, competition_name: str):
        if competition_name in self.competitions:
            request_data = request.get_json()

            if request_data:
                competition = self.competitions[competition_name]

                archer_class = request_data["class"]

                competition.remove_class(archer_class)

                return jsonify({
                    "status": "SUCCESS"
                })

    @staticmethod
    def existing_competitions():
        return jsonify({
            "status": "SUCCESS",
            "competitions": Competition.list_competitions()
        })