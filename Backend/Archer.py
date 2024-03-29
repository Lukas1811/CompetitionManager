
class Archer:
    def __init__(self, name: str, bow_type: str, archer_class: str, club: str):
        self.name = name
        self.bow_type = bow_type
        self.archer_class = archer_class
        self.club = club
        self.total_score = None
        self.__scores =[]

    def to_dict(self) -> dict:
        archer = dict()

        archer["name"] = self.name
        archer["bow"] = self.bow_type
        archer["class"] = self.archer_class
        archer["club"] = self.club
        archer["scores"] = self.__scores
        archer["total_score"] = self.get_total_score()

        return archer

    def add_score(self, score: int):
        self.__scores.append(score)

    def update_score(self, round_idx: int, score: int):
        round_idx -= 1

        try:
            self.__scores[round_idx] = score
        except:
            for index in range(0, (round_idx + 1) - len(self.__scores)):
                self.__scores.append(0)

            self.__scores[round_idx] = score


    def get_total_score(self):
        total_score = 0

        for score in self.__scores:
            total_score += score

        return total_score

    def calculate_score(self):
        self.total_score = self.get_total_score()
