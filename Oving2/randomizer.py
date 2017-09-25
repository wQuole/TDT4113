import random

def vaskeliste():
    boyza = ["William","Simon","Paal-Arthur"]
    oppgave = ["Bad&Vaskerom","Kjøkken","Stue&Gang"]
    uke = 37
    delegering = ''
    for u in range(52-uke):
        a = "Uke: " + str(uke + u) + " - "
        for x in range(0, 3, 1):
            delegering += str(a)
            delegering += random.choice(oppgave)
            delegering += ": "
            delegering += random.choice(boyza)
            delegering += "\n"
    return delegering

print(vaskeliste())



