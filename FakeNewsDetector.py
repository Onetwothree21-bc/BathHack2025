import random

def GenInitialPop():
    return 
def evalPopFitness():
    return 
def intiliseAtomProperties(Xs,Es):
    return [(sum(Xs)/len(Xs)),(sum(Es)/len(Es)),min(Es)]
def GenOrbitalNumber():
    return random.randint(0,15)
def GetPDF():
    return 
def DistrobuteViaPDF():
    return 


def DetBSk(kXs):
    return (sum(kXs)/len(kXs))
def DetBEk(kEs):
    return (sum(kEs)/len(kEs))
def GetXink(dist,k):
    values = []
    for i in range(0,len(dist)):
        if dist[i][k] == 1:
            values.append(i)
    return values
def FindLowLEk(Es):
    return min(Es)
def getValues(m,ks):
    values = []
    for i in range(0,len(ks)):
        values.append(m[ks[i]])
    return values


def DetPR():
    return 0.75
def DetParameters():
    return [random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1)]
def UpdateForE10():
    return
def UpdateForE11():
    return
def UpdateForE12():
    return 
def Genr(k):
    values = []
    for i in range(0,k):
        values.append(random.uniform(0, 1))
    return values

def UpdateEnergies():
    return


def ConstructArray():
    return 
def PullRandomR():
    return 
def GenVSolution():
    return
def GenSolutions():
    return
def FactorAnaysis():
    return 
def BestSolution():
    return 
def PullRandomX():
    return

def Replace():
    return

def Main(candidates):
    initial = GenInitialPop(candidates)
    energies = evalPopFitness(candidates)
    baseProperties = intiliseAtomProperties(candidates  )
    counter = 1
    while (counter < 1):
        n = GenOrbitalNumber()
        candidates.sort()
        pMatrix = DistrobuteViaPDF()
        for k in range(0,n):
            kXs = GetXink(initial)
            kEnergies = getValues(energies,kXs)
            kSolutions = getValues(candidates,kXs)
            BS = DetBSk(kSolutions)
            BE = DetBEk(kEnergies)
            Low = FindLowLEk(kXs) 
            for i in range(0,len(kSolutions)):
                photonRate = DetPR()
                paramA = DetParameters()
                if paramA[0] >= photonRate :
                    if kEnergies[i] >= BE:
                        kEnergies[i+1] = UpdateForE10(kEnergies[i],paramA,baseProperties,k)
                    else :
                        kEnergies[i+1] = UpdateForE11(kEnergies[i],paramA,BS,Low)
                else:
                    r = Genr()
                    kEnergies[i+1] = UpdateForE12(kEnergies[i],r)
        baseProperties = UpdateEnergies(candidates)

