import random
import matplotlib.pyplot as plt

__author__ = 'wQuole'

# ------------------------------------------- S T E I N _ S A K S _ P A P I R -----------------------------------------

# ------------------------- Spiller-klassen -------------------------------
# *******************_ T H E _ S U P E R C L A S S _**********************#
                                                                          #
class Player:                                                             #
    _info = {}                                                            #
                                                                          #
    _move = {0:"Stein",1:"Saks",2:"Papir"}                                #
                                                                          #                                                                 #
    def __init__(self, name):                                             #
        self.name = name                                                  #
        Player._info[self] = []                                           #
                                                                          #
    # Denne metoden velger hvilken aksjon som skal utføres (spille        #
    # stein, saks eller papir) og returnerer dette                        #
    def choose_action(self):                                              #
        return                                                            #
                                                                          #
    def receive_result(self,opponent,move):                               #
        Player._info[opponent].append(move)                               #
                                                                          #
    def __str__(self):                                                    #
        return self.name                                                  #
                                                                          #
#*************************************************************************#

# ---------------------------- Action-class -------------------------------
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

# ----------------------- Tilfeldig spiller -----------------------
class Random(Player):

    def __init__(self, name):
        Player.__init__(self, name)

    def choose_action(self,motstander):
        return Action(random.randint(0,2))

# ---------------------------- Sekvensiell  ----------------------------
class Sequential(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.c = 0

    def choose_action(self,opponont):
        action = Action(self.c%3)
        self.c += 1
        return action

# ---------------------------- Mest vanlig -------------------------------
class Most_Common(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    # Hvis motstander ikke har gjort noe trekk, gjør noe random
    def choose_action(self,motstander):
        motstander_trekk = Player._info[motstander]
        if len(motstander_trekk) == 0:
            return Action(random.randint(0,2))
        stein = motstander_trekk.count(Action(0))
        saks = motstander_trekk.count(Action(1))
        papir = motstander_trekk.count(Action(2))
        freq = [stein, saks, papir]
        freq_maks = [i for i, x in enumerate(freq) if x == max(freq)]
        if len(freq_maks) > 1:
            return Action(random.choice(freq_maks))
        return Action(motsatte(self,max(freq_maks)))
        #max_index = liste.index(max(liste)) #Finner index til trekket med høyest frekvens
        #return Action(motsatte(self,max_index))

# ------------------------------ Historiker ------------------------------
class Historian(Player):
    def __init__(self, name,husk):
        Player.__init__(self, name)
        self.husk = husk

    def choose_action(self,opponent):
        sequence = Player._info[opponent]
        if len(sequence) < self.husk:
            return Action(random.randint(0, 2))

        sub_seq = sequence[-self.husk:]
        freq = [0,0,0]
        for act in range(len(sequence) - self.husk -1, -0, -1):
            if sub_seq == sequence[act:act + self.husk]:
                move = sequence[act + self.husk]
                freq[move.getAction()] += 1
        if (max(freq)) < 1:
               return Action(random.randint(0, 2))
        choice = motsatte(self,freq.index(max(freq)))
        return Action(choice)

# ****************ENKELTSPILL CLASS****************
#Setter opp en enkelt kamp
class EnkeltSpill:

    def __init__(self,spiller1,spiller2):
        self.s1 = spiller1
        self.s2 = spiller2
        #Poeng
        self.ps1 = 0
        self.ps2 = 0

    #Utfører spillet mellom spiller 1 og 2
    #Spørr hver spiller om deres valg
    #Bestem resultat. 1 poeng til vinner, 0 til taper. 0.5 til hver ved uavgjort
    #Rapporter valgene og resultatene tilbake til spiller
    def gjennomfør_spill(self):
        self.a1 = self.s1.choose_action(self.s2)
        self.a2 = self.s2.choose_action(self.s1)
        #print(self.s1,"\t:",self.a1)
        #print(self.s2,"\t:",self.a2)
        if self.a1 == self.a2:
            self.ps1,self.ps2 = 0.5,0.5
        elif self.a1 > self.a2:
            self.ps1,self.ps2 = 1,0
        else:
            self.ps1,self.ps2 = 0,1

        self.s1.receive_result(self.s2, self.a2)
        self.s2.receive_result(self.s1, self.a1)

    def winner(self):
        if self.ps1 == self.ps2:
            return 'Ingen'
        elif self.ps1 > self.ps2:
            return self.s1
        else:
            return self.s2

    def get_score(self):
        return [self.ps1,self.ps2]

    def __str__(self):
        return str(self.s1) + ": " + str(self.a1) + ". " + str(self.s2) + " : " + \
               str(self.a2) + " --> " + str(self.winner()) + " vinner"


# ****************MANGESPILL CLASS****************
class MangeSpill:

    def __init__(self,spiller1,spiller2,antall_spill):
        self.s1 = spiller1
        self.s2 = spiller2
        self.antall_spill = antall_spill

    def arranger_enkeltspill(self):
        return EnkeltSpill(self.s1,self.s2)

    def arranger_turnering(self):
        tot_s1 = 0
        tot_s2 = 0
        gevinst_s1 = []
        gevinst_s2 = []
        x_akse = []
        count = 0
        for x in range(0,self.antall_spill):
            enkel = self.arranger_enkeltspill()
            enkel.gjennomfør_spill()
            score = enkel.get_score()
            tot_s1 += score[0]
            tot_s2 += score[1]

            ##PYPLOT##
            count+=1
            x_akse.append(count)
            gevinst_s1.append(tot_s1/count)
            gevinst_s2.append(tot_s2/count)

            print(enkel)

        ##PYPLOT##
        plt.plot(x_akse,gevinst_s1)
        plt.plot(x_akse,gevinst_s2)
        plt.axis([0,self.antall_spill,0,1])
        plt.grid(True)
        plt.axhline(y=0.5,linewidth=0.5, color="r")
        plt.xlabel("Antall Spill")
        plt.ylabel("Win%: " + str(self.s1))
        plt.title("Dette er en grafisk representasjon")
        plt.show()

        print("\nTotal score i turneringen:\n" + str(self.s1) + ": " + str(tot_s1) + " poeng" +
              "\n" + str(self.s2) + ": " + str(tot_s2) + " poeng")

#Hjelpefunksjon
def motsatte(self,num):
    a = {0: 2, 1: 0, 2: 1}
    return a[num]

def main():
    s1 = Historian('William',3)
    s2 = Most_Common('Kristoffer')

    mange = MangeSpill(s1,s2,2000)
    mange.arranger_turnering()

    #enkle = EnkeltSpill(s1,s2)
    #enkle.gjennomfør_spill()
    #enkle.gjennomfør_spill()
    #enkle.get_score()
    #enkle.winner()
    #print(enkle.winner())

main()