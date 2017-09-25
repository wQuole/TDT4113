import math

def func(n):
    print("Sannsynligheten for å få ingen billedkort, når du får utdelt",n," er:\n",round((math.factorial(36)/math.factorial(36-n))/
                 (math.factorial(52)/math.factorial(52-n)),
                 5))

#print(func(10))

freq = [2,2,1]

freq_maks = [i for i, x in enumerate(freq) if x == max(freq)]
print(freq_maks)