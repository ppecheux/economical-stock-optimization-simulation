# coding: utf-8 

"""

On s’intéresse au stock de produits P1, le plus vendu.
On considère que la demande hebdomadaire de produits 
P1 peut être modélisée par une loi Normale N(155,38.9)

stock de sécurité : SS= alpha*sigma
demande ~ N(155,60)
(demande-155)/(60/sqrt(n)) ~ N(0,1)
P(-U(1-a/2)<demande-155)/(60/sqrt(n))< U(1-a/2))=1-a

alpha = étant fixé
"""
import numpy as np
import matplotlib.pyplot as plt

class Stock:
    '''représente l'état du stock sur les semaines'''


    def __init__(self,serviceCible,stockCible,ListeSemainesDeStock):
        self.sc=float(serviceCible)#proportion de clients servis
        self.semaines=ListeSemainesDeStock#liste de stock
        self.dechet=0.0#on aurait pu mettre comme une semaine suplémentaire...
        self.nbNonSatifait = 0.0
        self.stockCible = float(stockCible)
        self.fournis= float(self.stockTotal())

    def stockTotal(self):
        somme=0
        for i in self.semaines:
            somme+=i
        return somme

    def nouvelleSemaine(self,demande):
        #On cherche à répondre à la demande
        #On considère qu'on doit livrer qu'un seul client
        temp=[]
        for i in self.semaines:
            
            if i>demande :
                i-=demande
                demande=0
            else:
                demande-=i
                i=0

            temp.append(i)

        if demande>0 :
            self.nbNonSatifait+= 1

        self.semaines=temp

        #ON décale les semaines
        self.dechet+=self.semaines[len(self.semaines)-1]
        for i in range (0, len(self.semaines) - 1):
            self.semaines[len(self.semaines)-i-1]=self.semaines[len(self.semaines)-i-2]
        
        #On initialise la nouvelle semaine
        self.semaines[0]=self.stockCible-self.stockTotal()#TODO #c'est bon
        self.fournis+=self.semaines[0]
    
    def printStock(self):
        print("\nmon stock total actuel est de ")
        print(self.stockTotal())


nbSemPermenption = 3
ListeSemainesDeStock = np.zeros(nbSemPermenption)





def simulerSemainesStockCible(nbSemaines,stockCible,demandes):
    ListeSemainesDeStock[0]=stockCible
    monStock=Stock(1,stockCible,ListeSemainesDeStock)

    for i in demandes:
        monStock.nouvelleSemaine(i)

    serviceCibleReel = float(1 - (float(monStock.nbNonSatifait)/nbSemaines))
   
    return serviceCibleReel

def dechetsSemainesStockCible(nbSemaines,stockCible,demandes):
    ListeSemainesDeStock[0]=stockCible
    monStock=Stock(1,stockCible,ListeSemainesDeStock)

    for i in demandes:
        monStock.nouvelleSemaine(i)
    
    tauxDechet=0.0
    try:
        tauxDechet = float(monStock.dechet)/monStock.fournis
    except:
        return -1

    print([tauxDechet,monStock.dechet,monStock.fournis,monStock.stockTotal()])
    return tauxDechet#semble trop faible

#dechetsSemainesStockCible(10,155)

def simulerTabStockCible(nbSemaines,tabStockCible,mesDemandes):
    tabService = []
    for i in tabStockCible:
        tabService.append( simulerSemainesStockCible(nbSemaines,i,mesDemandes))
    return(tabService)

def dechetTabStockCible(nbSemaines,tabStockCible,mesDemandes):
    tabDechet = []
    for i in tabStockCible:
        tabDechet.append( dechetsSemainesStockCible(nbSemaines,i,mesDemandes))
    return(tabDechet)

#dechetTabStockCible(10,[3,2],[1550,0])

def simulationPousse():

    tabStockCible=np.arange(0,500,10)
    mu, sigma = 155, 60 # demande moyenne et equart type de la demande moyenne

    nbsemaine=10000
    mesDemandes = np.random.normal(mu, sigma, nbsemaine)

    tabServiceSimule =simulerTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    dechets = dechetTabStockCible(nbsemaine,tabStockCible,mesDemandes)

    plt.ylabel("Service Reel Simule")
    plt.xlabel("Stock Cible")
    plt.plot(tabStockCible,tabServiceSimule,'ro')
    plt.plot(tabStockCible,dechets)
    print(tabServiceSimule)
    print(dechets)
    plt.show()

simulationPousse()




#print(dechetsSemainesStockCible(100,200))


#print(serviceCibleReel)
