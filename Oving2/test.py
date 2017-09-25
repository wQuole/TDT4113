import random

# ------------------------- Spiller-klassen -------------------------  **********T H E _ S U P E R C L A S S _**********
class Player:
    _info = {}

    _move = {0:"Stein",1:"Saks",2:"Papir"}


    def __init__(self, name):
        self.name = name
        Player._info[self] = []

    # Denne metoden velger hvilken aksjon som skal utføres (spille
    # stein, saks eller papir) og returnerer dette
    def choose_action(self):
        return

    def receive_result(self,opponent,move):
        Player._info[opponent].append(move)

    def getName(self,name):
        self.name = name

    def __str__(self):
        return self.name

# ---------------------------- Action-class ----------------------------
class Action:
    def __init__(self, num):
        # ref: _move
        self.action = num

    def __eq__(self, other):
        return other.action == self.action

    # Greater than
    def __gt__(self, other):
        a = {0: 2, 1: 0, 2: 1}
        return a[self.action] != other.action

    def __str__(self):
        ordliste = ["Stein", "Saks", "Papir"]
        return ordliste[self.action]

    def getAction(self):
        return self.action


# ------------------------------ Historiker ------------------------------

class Historian(Player):
    def __init__(self, name,husk):
        Player.__init__(self, name)
        self.husk = husk

    def choose_action(self,opponent):
        sequence = Player._info[opponent]
        if len(sequence) < self.husk:
            return Action(random.randint(0,2))

        sub_seq = sequence[-self.husk:]
        freq = [0,0,0]




def main(husk):
    sequence = ["Stein", "Saks", "Papir"]
    if len(sequence) < husk:
        return random.randint(0, 2)

    sub_seq = sequence[-husk:]
    freq = [0, 0, 0]

