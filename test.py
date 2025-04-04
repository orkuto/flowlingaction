class player:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3

    
    def change(self,a):
        self.a = a



class kure:
    def __init__(self):
        self.k = 1
        self.g = 4
        self.c = 6

    def kore(self):
        self.k = 1
        self.g = 4
        self.c = 6


ks = player()

ku = kure()

print(ks.b)

ks.change(ku)

print(ks.a.g)

for i in range(3):
    print(i)