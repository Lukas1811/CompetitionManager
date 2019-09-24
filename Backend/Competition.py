import json
from os import listdir
from os.path import abspath
from datetime import datetime

from Backend.Archer import Archer
from Backend.logger import Logger as log


class Competition:
    def __init__(self, name: str, path: str):
        self.name = name
        self.description = ""
        self.date = ""
        self.path = path
        self.config = dict()
        self.bow_types = list()
        self.archer_classes = list()
        self.archers = list()
        self.creation_date = datetime.now()

    def set_description(self, new_description: str):
        self.description = new_description

    def set_date(self, new_date: str):
        self.date = new_date

    def set_name(self, name: str):
        self.name = name

    def add_archer(self, name: str, bow_type: str, archer_class: str, club: str):
        if name not in self.archers:
            if bow_type in self.bow_types:
                if archer_class in self.archer_classes:
                    new_archer = Archer(name,
                                        bow_type,
                                        archer_class,
                                        club)

                    self.archers.append(new_archer)
                else:
                    log.warn("Class {0} does not exists!".format(archer_class))
            else:
                log.warn("Bow {0} does not exists!".format(bow_type))
        else:
            log.warn("Archer {0} already exists!".format(name))

    def remove_archer(self, name: str):
        if name in self.archers:
            self.archers.remove(name)

    def add_bow(self, name: str):
        if name not in self.bow_types:
            self.bow_types.append(name)
        else:
            log.warn("Bow {0} already exists!".format(name))

    def remove_bow(self, name: str):
        if name in self.bow_types:
            self.bow_types.remove(name)
        else:
            log.warn("Bow {0} does not exist!".format(name))

    def add_class(self, name: str):
        if not name in self.archer_classes:
            self.archer_classes.append(name)
        else:
            log.warn("Class {0} already exists!".format(name))

    def remove_class(self, name: str):
        if name in self.archer_classes:
            self.archer_classes.remove(name)
        else:
            log.warn("Class {0} does not exist!".format(name))

    def import_archers(self, archer_file: str):
        with open(archer_file, "r", encoding='utf-8') as file:
            file = json.load(file)
            archers = file["Archers"]
            bow_types = file["Bows"]
            archer_classes = file["Classes"]
            archer_count = 0

            for bow in bow_types:
                self.add_bow(bow_types[bow])

            for archer_class in archer_classes:
                self.add_class(archer_classes[archer_class])

            for archer in archers:
                self.add_archer(archers[archer]["name"],
                                archers[archer]["bow"],
                                archers[archer]["class"],
                                archers[archer]["club"])

                archer_count += 1

            log.info("Loaded {0} archers, from file: {1}".format(archer_count, archer_file))

    def to_sorted_dict(self) -> dict:
        sorted_dict = dict()

        for archer in self.archers:
            bow_type = archer.bow_type
            archer_class = archer.archer_class

            if bow_type not in sorted_dict:
                sorted_dict.update({bow_type: dict()})

            if archer_class not in sorted_dict[bow_type]:
                sorted_dict[bow_type].update({archer_class: list()})

            sorted_dict[bow_type][archer_class].append(archer.to_dict())

            sorted_dict[bow_type][archer_class].sort(key=lambda entry: entry["total_score"])

        return sorted_dict

    def save(self):
        config = self.to_dict()

        with open(self.path, "w") as file:
            file.write(json.dumps(config, indent=4))

    def to_dict(self) -> dict:
        config = dict()

        path_elements = self.path.split("/")
        path_elements = path_elements[: len(path_elements) - 1]

        self.path = ""

        for element in path_elements:
            self.path += element + "/"

        self.path += self.name

        config["name"] = self.name
        config["date"] = self.date
        config["description"] = self.description
        config["path"] = self.path
        config["bows"] = self.bow_types
        config["classes"] = self.archer_classes
        config["archers"] = {}

        for archer_obj in self.archers:
            archer = archer_obj.to_dict()
            config["archers"].update({archer["name"]: archer})

        print(config)

        return config

    @staticmethod
    def new_competition(name: str):
        return Competition(name, "../Database/" + name)

    @staticmethod
    def load_competition(config_path: str):
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

            competition = Competition(config["name"], config["path"])
            try:
                competition.date = config["date"]
                competition.description = config["description"]
            except:
                pass
            competition.bow_types = config["bows"]
            competition.archer_classes = config["classes"]

            archers = []

            for archer in config["archers"]:
                archer_object = Archer( config["archers"][archer]["name"],
                                        config["archers"][archer]["bow"],
                                        config["archers"][archer]["class"],
                                        config["archers"][archer]["club"])

                for score in config["archers"][archer]["scores"]:
                    archer_object.add_score(score)

                archer_object.calculate_score()

                archers.append(archer_object)

            competition.archers = archers

            log.info("Loaded competition {0}!".format(competition.name))

            return competition

    @staticmethod
    def list_competitions():
        database_dir = abspath("./Database")
        files = listdir(database_dir)
        files.remove("__init__.py")

        return files



