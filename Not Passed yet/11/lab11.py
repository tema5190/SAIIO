import json
from functools import reduce
import numpy as np
import random
from math import pow

def setMainDiagInf(m):
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            if(m[i,j]==0):
                m[i,j]=0.000001
    return m+np.diag([float('inf')]*m.shape[0])

def getChance(v,g,ph,alpha,beta,visited):
    notVisited = [i for i,j in enumerate(visited) if not j]
    costs = [j for i,j in enumerate(g[v,:].A1) if i in notVisited]
    pherams = [pow(j,alpha) for i,j in enumerate(ph[v,:].A1) if i in notVisited]
    costChance = [pow(i,beta) for i in costs]
    total = sum([i*j for i,j in zip(costChance,pherams)])
    return [i*j/total for i,j in zip(costChance,pherams)],notVisited

def chooseNextV(chance,verts):
    rnd = random.random()
    #print(rnd)
    i=0
    s=chance[i]
    while s<rnd:
        i+=1
        s+=chance[i]
    return verts[i]

def getAntPath(g,ph,alpha,beta):
    path=[0]
    v = 0
    visited = [False]*g.shape[0]
    visited[v]=True
    for i in range(g.shape[0]-1):
        chanse,verts = getChance(v,g,ph,alpha,beta,visited)
        nextV = chooseNextV(chanse,verts)
        visited[nextV]=True
        path.append(nextV)
        v=nextV
    path.append(0)
    return path

def getPathCost(g,path):
    s=0
    for i in range(len(path)-1):
        s+=g[path[i],path[i+1]]
    return s

def updatePh(path,g,ph,q=6,p=0.2):
    cost = getPathCost(g,path)
    deltaPh = q/cost
    for i in range(len(path)-1):
        ph[path[i],path[i+1]]=(1-p)*ph[path[i],path[i+1]]+deltaPh

#alpha - pheramons
#beta - cost
def antAlgorithm(g,alpha=10,beta=1,q=1):
    random.seed(1)
    n = g.shape[0]
    ph = np.matrix([[1.0]*n for i in range(n)],dtype=float)
    mCost=float('inf')
    mPath=[]
    for i in range(q):
        path = getAntPath(g,ph,alpha,beta)
        cost = getPathCost(g,path)
        updatePh(path,g,ph)
        # print(cost)
        if(cost<mCost):

            mCost=cost
            mPath = path
        #print(i)

    print(mPath)
    print(mCost)

if __name__ == "__main__":
    m = json.loads(open("data.txt").read())
    m = np.matrix(m,dtype=float)

    m = setMainDiagInf(m)
    #print(m)
    antAlgorithm(m,q=1000)
    #path = [1,8,4,7,5,6,9,10,3,2,1]
    #path = list(map(lambda x:x-1,path))
    #print(getPathCost(m,path))




