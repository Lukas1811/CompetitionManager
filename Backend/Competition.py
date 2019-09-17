import json

from Backend.Archer import Archer
from Backend.logger import Logger as log


class Competition:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.config = dict()
        self.bow_types = list()
        self.archer_classes = list()
        self.archers = dict()

    def add_archer(self, name: str, bow_type: str, archer_class: str):
        if name not in self.archers:
            if bow_type in self.bow_types:
                if archer_class in self.archer_classes:
                    new_archer = Archer(name,
                                        bow_type,
                                        archer_class)

                    self.archers.update({name: new_archer})
                else:
                    log.warn("Class {0} does not exists!".format(archer_class))
            else:
                log.warn("Bow {0} does not exists!".format(bow_type))
        else:
            log.warn("Archer {0} already exists!".format(name))

    def add_bow(self, name: str):
        if name not in self.bow_types:
            self.bow_types.append(name)
        else:
            log.warn("Bow {0} already exists!".format(name))

    def add_class(self, name: str):
        if not name in self.archer_classes:
            self.archer_classes.append(name)
        else:
            log.warn("Class {0} already exists!".format(name))

    def import_archers(self, archer_file: str):
        with open(archer_file, "r") as file:
            archers = json.load(file)
            archer_count = 0

            for archer in archers:
                self.add_archer(archer["name"],
                                archer["bow"],
                                archer["class"])

                archer_count += 1

            log.info("Loaded {0} archers, from file: {1}".format(archer_count, archer_file))

    def to_sorted_dict(self) -> dict:
        sorted_dict = dict()

        for archer in self.archers:
            bow_type = self.archers[archer].bow_type
            archer_class = self.archers[archer].archer_class

            if bow_type not in sorted_dict:
                sorted_dict.update({bow_type: dict()})

            if archer_class not in sorted_dict[bow_type]:
                sorted_dict[bow_type].update({archer_class: list()})

            sorted_dict[bow_type][archer_class].append(self.archers[archer].to_dict())

            sorted_dict[bow_type][archer_class].sort(key=lambda entry: entry["total_score"])

        return sorted_dict

    def save(self):
        config = self.to_dict()

        with open(self.path, "w") as file:
            file.write(json.dumps(config, indent=4))

    def to_dict(self) -> dict:
        config = dict()

        config["name"] = self.name
        config["path"] = self.path
        config["bows"] = self.bow_types
        config["classes"] = self.archer_classes
        config["archers"] = self.archers

        print(config)

        for archer_obj in self.archers:
            archer = self.archers[archer_obj].to_dict()
            config["archers"].update({archer["name"]: archer})

        return config

    @staticmethod
    def new_competition(name: str):
        return Competition(name, "../Database/" + name)

    @staticmethod
    def load_competition(config_path: str):
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

            competition = Competition(config["name"], config["path"])
            competition.bow_types = config["bows"]
            competition.archer_classes = config["classes"]
            competition.archers = config["archers"]

            log.info("Loaded competition {0}!".format(competition.name))

            return competition
