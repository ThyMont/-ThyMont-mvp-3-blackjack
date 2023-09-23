cards = {'ACE': 1,
         '2': 2,
         '3': 3,
         '4': 4,
         '5': 5,
         '6': 6,
         '7': 7,
         '8': 8,
         '9': 9,
         '0': 10,
         'JACK': 11,
         'QUEEN': 12,
         'KING': 13
         }


class Player():
    soft_score: int = 0
    score: int = 0
    win: bool = False
    lose: bool = False
    cards = []

    def add_card(self, value: str):
        self.score += cards[value]
        if (value == 'ACE'):
            self.soft_score += 10
        else:
            self.soft_score += cards[value]
        if (self.soft_score == 21 or self.score == 21):
            self.win = True
            self.lose = False
        elif (self.score > 21):
            self.win = False
            self.lose = False
