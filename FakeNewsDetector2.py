import random
import numpy as np
import scipy
from scipy.stats import norm
import copy
import math



####### Make better
def CostFunction(x):
    return np.sum(x**2)      
###########



VarNumber = 190                           
VarMin = -10 * np.ones(VarNumber)       
VarMax = 10 * np.ones(VarNumber)   

def GenInitialPop(l,x):
    candidates = x
    energies = []
    for i in range(l):
        #candidates.append(np.random.uniform(VarMin, VarMax, VarNumber))
        energies.append(CostFunction(candidates[i]))      
    #global VarNumber
    #VarNumber = length  
    #global VarMin 
    #VarMin = -10 * np.ones(VarNumber)       
    #global VarMax 
    #VarMax = 10 * np.ones(VarNumber)
    return (candidates,energies)
def intiliseAtomProperties(candidates,energies):
    sortedIndices = np.argsort(energies)
    energies = np.array(energies)[sortedIndices] 
    candidates = np.array(candidates)[sortedIndices]  
    bestPop = candidates[0, :]
    meanPop = np.mean(candidates, axis=0)
    return (candidates,energies,bestPop,meanPop)

def GenOrbitalNumber():
    return random.randint(1,5)
#same here
def DistrobuteViaPDF(size,n):
    normInput = np.arange(1,n+1)
    normDist = norm.pdf(normInput,0,n/6)
    normDistm = np.zeros((5,n))
    normDistm[0,:] = normDist
    normDistm[1,:] = normDistm[0,:] / np.sum(normDistm[0,:])
    normDistm[2,:] = size * normDistm[1,:]
    normDistm[3,:] = np.round(normDistm[2,:])
    normDistm[4,:] = np.cumsum(normDistm[3,:])
    LayCol= np.concatenate(([0], normDistm[4, :]))
    LayCol[LayCol > size] = size
    return LayCol


def DetBEk(kEs):
    if (len(kEs) == 0):
        return 0
    return (sum(kEs)/len(kEs))
def getValues(m,ks,k):
    return m[int(ks[k]+1):int(ks[k+1])]


def DetPR():
    return 0.01
def DetParameters():
    return [random.uniform(0, 1),np.random.uniform(0, 1, VarNumber),random.uniform(0, 1),random.uniform(0, 1)]
def UpdateForE10(Ek, paramA, baseProperties, k):
    temp = Ek + (paramA[1] * (paramA[2]*baseProperties[2]-paramA[3]*baseProperties[3])/k)
    temp = np.maximum(temp, VarMin)
    temp = np.minimum(temp, VarMax)
    return temp
def UpdateForE11(Ek, paramA, baseProperties):
    temp = Ek + (paramA[1] * (paramA[2]*baseProperties[2]-paramA[3]*baseProperties[3]))
    temp = np.maximum(temp, VarMin)
    temp = np.minimum(temp, VarMax)
    return temp

def UpdateEnergies(base,cf,ef,bestEnergy,n,k):
    candidates = base[0]
    energy = base[1]
    candidates = np.vstack([candidates, cf])
    energy = np.vstack([energy, ef])
    SortOrder = np.argsort(energy[:, 0]) 
    energy = energy[SortOrder]
    candidates = candidates[SortOrder]
    base2 = candidates[0, :]
    BestCost = energy[0, 0]
    base3 = np.mean(candidates, axis=0)
    candidates = candidates[:19000, :23000]
    energy = energy[:n, :]
    e2 = np.zeros((n))
    for i in range(0,len(energy)):
        e2[i] = np.mean(energy[i])
    bestEnergy[k] = BestCost
    

    # Show Iteration Information
    print(f"Iteration {k}: Best Cost = {bestEnergy[k, 0]}")
    return (candidates,e2,base2,base3)


def ConstructArray(Q, J):
    return [[1,1,1,1],[1,2,2,2],[1,3,3,3],[2,1,2,3],[2,2,3,1],[2,3,1,2],[3,1,3,2],[3,2,1,3],[3,3,2,1]]




    M = (2*Q)+J-1
    basic_cols = []

    for k in range(1, J + 1):
        j = (Q ** (k - 1) - 1) // (Q - 1) + 1
        col = np.zeros(M, dtype=int)

        for i in range(1, M + 1):
            exponent = J - k
            denominator = Q ** exponent if exponent >= 0 else 0
            if denominator != 0:
                col[i - 1] = ((i - 1) // denominator) % Q

        basic_cols.append(col)
    OA = np.column_stack(basic_cols)
    #for k in range(1, J):
    #    j = (Q ** (k - 1) - 1) // (Q - 1) + 1
    #    for s in range(0, j):
    #        for t in range(0, Q):
    #            new_col = (OA[:, s - 1] * t + OA[:, j - 1]) % Q
    #            OA = np.column_stack((OA, new_col))
    for i in range(0,M):
        for j in range(0,len(OA[i])):
            OA[i][j] +=1
    return OA



def PullRandomR(Solutions):
    r = random.randint(0,len(Solutions)-1)
    return Solutions[r]
def GenVSolution(Solutions):
    return PullRandomR(Solutions) + np.random.uniform(0,1)*(PullRandomR(Solutions)-PullRandomR(Solutions))
def GenSolutions(M,V):
    return V @ M
def FactorAnaysis(M,Q,J):
    if not(isinstance(M[0],np.ndarray)):
        return M
    fValues = []
    # run each through cost function
    for i in range(0,len(M)):
        fValues.append(CostFunction(M[i]))
    # Calculate H function for each
    shadowM = np.zeros(shape=(Q,J))
    for i in range(0,Q):
        for j in range(0,J):
            count = 0
            numCount = 0
            for k in range(0,len(M)):
                if M[k][Q] == J:
                    count += fValues[k]
            if numCount != 0:
                count = count/numCount
            else:
                count = 100000
            shadowM[Q][J] = count

    # Determine 'best' senario
    bestValues = []
    bi = []
    bj = []
    for i in range(0,len(shadowM)):
        bestColValue = 1000000
        besti = 0
        bestj = 0
        for j in range(0,len(shadowM[0])):
            if shadowM[i][j] < bestColValue:
                bestColValue = shadowM[i][j]
                besti = i
                bestj = j
        bi.append(besti)
        bj.append(bestj)
    
    bestValues.append(M[0][(bi+1)*Q])
    for i in range(0,len(bi-1)):
        bestValues.append(M[i+1][bi])
    return bestValues
def BestSolution(Solutions):
    return min(Solutions)

def Replace():
    return

def Main2(x):
    x.toarray()
    global VarNumber 
    VarNumber = len(x)                           
    global VarMin
    VarMin = -10 * np.ones(VarNumber)       
    global VarMax
    VarMax = 10 * np.ones(VarNumber)  
    l = len(x[0])
    initial = GenInitialPop(l,x)
    baseProperties = intiliseAtomProperties(initial[0],initial[1])
    candidates = baseProperties[0]
    energies = baseProperties[1]
    counter = 1
    kSolutionsf = copy.deepcopy(candidates)
    kEnergiesf = copy.deepcopy(energies)
    bestEnergys = np.zeros(shape=(500,1))
    while (counter < 499):
        #### AOS
        candidates = baseProperties[0]
        energies = baseProperties[1]
        counter +=1
        n = GenOrbitalNumber()
        candidates.sort()
        pMatrix = DistrobuteViaPDF(len(candidates), n)
        kSolutionst = copy.deepcopy(candidates)
        kEnergiest = copy.deepcopy(energies)
        for k in range(1,n+1):
            kEnergies = getValues(energies,pMatrix,k-1)
            kSolutions = getValues(candidates,pMatrix,k-1)
            BE = DetBEk(kEnergies)
            for i in range(0,len(kEnergies)):
                photonRate = DetPR()
                paramA = DetParameters()
                if paramA[0] >= photonRate :
                    if np.all(kEnergies[i] >= BE): #all?
                        kSolutionst[i,:] = UpdateForE10(kSolutions[i],paramA,baseProperties,k)
                        kEnergiest[i] = CostFunction(kSolutionst[i,:])
                    else :
                        kSolutionst[i,:] = UpdateForE11(kSolutions[i],paramA,baseProperties)
                        kEnergiest[i] = CostFunction(kSolutionst[i,:])
                else:
                    kSolutionst[i,:] = np.random.uniform(VarMin, VarMax, VarNumber)
                    kEnergiest[i] = CostFunction(kSolutionst[i,:])
            kEnergiesf = np.vstack([kEnergiesf,kEnergiest])
            kSolutionsf = np.vstack([kSolutionsf,kSolutionst])

                
        baseProperties = UpdateEnergies(baseProperties,kSolutionsf,kEnergiesf,bestEnergys,l,counter)

        #### Orthogonal Search
        arraySizeQ = 3
        arraySizeJ = 4
        oArray = ConstructArray(arraySizeQ,arraySizeJ)
        solR = PullRandomR(baseProperties[0])[:9]
        solV = GenVSolution(baseProperties[0])[:9]
        solsM = GenSolutions(oArray,solR)+GenSolutions(oArray,solV)
        solM1 = FactorAnaysis(solsM,arraySizeQ,arraySizeJ)
        bestSolX = BestSolution(solM1)
        randomX = PullRandomR(baseProperties[0])
        if (bestSolX > CostFunction(randomX)):
            baseProperties[0][random.randint(0,len(solsM)-1)] = bestSolX
        
    

