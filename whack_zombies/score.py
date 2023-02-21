from .constants import LevelConstants, GameConstants


class Score:
    """
    Handles the scoring for the player
    """

    def __init__(self):
        self.hits = 0
        self.misses = 0


    @property
    def score(self):
        score = (self.hits - (self.misses / 2)) * 2
        if score < 0:
            score = 0
        return score

    def hit_rate(self):
        if self.misses + self.hits == 0:
            return 0
        else:
            return int((self.hits/(self.misses + self.hits))*100)

    @property
    def level(self):
        if self.score < 0:
            return 1
        else:
            return int(1 + (self.score // LevelConstants.level_gap))

    @property
    def attempts(self):
        return self.hits + self.misses

    def show_score(self):
        text = "{}".format(int(self.score))
        return text

    def show_hit_rate(self):
        text = "{} %".format(self.hit_rate())
        return text

    def show_hits(self):
        text = "{}".format(int(self.hits))
        return text

    def show_misses(self):
        text = "{}".format(int(self.misses))
        return text

    def hit(self):
        self.hits += 1

    def miss(self):
        self.misses += 1
